import os
import random
import re
from datetime import datetime
import pytz
from django.http import FileResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView

from common.SMS import AliYunSMS
from .models import Users, Address, AuthCode
from .permissions.Address import AddressPermission
from .permissions.users import UserPermission
from .serializers.address import AddressSerializer
from .serializers.users import UserSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")


class RegisterView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        password_confirmation = request.data.get('password_confirmation')

        if not all([username, password, email, password_confirmation]):
            return Response({'error': "缺少必要参数"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if Users.objects.filter(username=username).exists():
            return Response({'error': "用户已存在"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if password != password_confirmation:
            return Response({'error': "两次输入的密码不一致"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not (6 <= len(password) <= 18):
            return Response({'error': "密码长度应在6-18位之间"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if Users.objects.filter(email=email).exists():
            return Response({'error': "该邮箱已注册"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return Response({'error': "邮箱格式错误"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        obj = Users.objects.create_user(username=username, email=email, password=password)
        res = {
            'id': obj.id,
            'username': username,
            'email': email
        }
        return Response(res, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        result = serializer.validated_data
        result['id'] = serializer.user.id
        result['mobile'] = serializer.user.mobile
        result['email'] = serializer.user.email
        result['username'] = serializer.user.username
        result['token'] = result.pop('access')
        return Response(result, status=status.HTTP_200_OK)


class UserView(GenericViewSet, mixins.RetrieveModelMixin):

    queryset = Users.objects.all()
    serializer_class = UserSerializer
    # 设置认证用户才能有权访问
    permission_classes = [IsAuthenticated, UserPermission]

    def upload_avatar(self, request):
        """上传用户头像"""
        avatar = request.data.get('avatar')
        if not avatar:
            return Response({'error': '上传失败，文件不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if avatar.size > 1024*300:
            return Response({'error': '上传失败，文件大小不能超过300kb'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = request.get_object()
        serializer = self.get_serializer(user, data={"avatar": avatar}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'url': serializer.data['avatar']}, status=status.HTTP_200_OK)

    @staticmethod
    def verify_auth_code(code, code_id, mobile):
        """验证短信验证码"""
        if not code:
            return {'error': '验证码不能为空'}
        if not code_id:
            return {'error': '验证码ID不能为空'}
        if not mobile:
            return {'error': '手机号不能为空'}
        obj = AuthCode.objects.filter(id=code_id, code=code, mobile=mobile)
        if obj:
            time = (datetime.now().astimezone() - obj.created_time.astimezone()).seconds
            obj.delete()
            if time > 180:
                return {'error': '验证码已过期, 请重新获取'}
        else:
            return {'error': '验证码错误'}

    def bind_mobile(self, request):
        """绑定手机号"""
        code = request.data.get('code')
        codeID = request.data.get('codeID')
        mobile = request.data.get('mobile')
        if result := self.verify_auth_code(code, codeID, mobile):
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if Users.objects.filter(mobile=mobile).exists():
            return Response({'error': '手机号已被用户绑定'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = request.user
        user.mobile = mobile
        user.save()
        return Response({'message': "绑定成功"}, status=status.HTTP_200_OK)

    def unbind_mobile(self, request):
        """解绑手机号"""
        code = request.data.get('code')
        codeID = request.data.get('codeID')
        mobile = request.data.get('mobile')
        if result := self.verify_auth_code(code, codeID, mobile):
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = request.user
        if user.mobile != mobile:
            return Response({'error': '当前用户没有绑定该号码'}, status=status.HTTP_400_BAD_REQUEST)
        user.mobile = ''
        user.save()
        return Response({'message': '解绑成功'}, status=status.HTTP_200_OK)


class FileView(APIView):
    """获取头像文件"""
    def get(self, request, name):
        path = settings.MEDIA_ROOT / name
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'))
        return Response({'error': '没有找到该文件'}, status=status.HTTP_404_NOT_FOUND)


class AddressView(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin,
                  mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    """地址管理视图"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    permission_classes = [IsAuthenticated, AddressPermission]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def set_default_address(self, request):
        obj = self.get_object()
        obj.is_default = True
        obj.save()
        queryset = self.get_queryset().filter(user=request.user)
        for item in queryset:
            if item != obj:
                item.is_default = False
                item.save()
        return Response({'message': '设置成功'}, status=status.HTTP_200_OK)


class SendSMSView(APIView):
    """短信验证码"""

    throttle_classes = (AnonRateThrottle,)

    def post(self, request):
        mobile = request.data.get('mobile')
        res = re.match(r"^1(3[0-9]|5[0-3,5-9]|7[1-3,5-8]|8[0-9])\d{8}$", mobile)
        if not res:
            return Response({'error': '无效的手机号码'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        code = self.get_random_code()
        result = AliYunSMS(mobile=mobile, sms_code=code).send_msg()
        if result['code'] == 'YES':
            obj = AuthCode.objects.create(mobile=mobile, code=code)
            result['codeID'] = obj.id
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_random_code():
        return ''.join(random.sample('0123456789', 6))



