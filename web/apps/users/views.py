import os
import re

from django.conf import settings
from django.http import FileResponse
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView

from common.default_permission import BasePermission, AdminPermission
from .models import Users, Address, Area
from .serializers import AddressSerializer, AreaSerializer, UserSerializer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")


class RegisterView(APIView):

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        password_confirmation = request.data.get('password_confirmation')
        uuid = request.data.get('uuid')
        image_code = request.data.get('image_code')

        if not all([username, password, email, password_confirmation, uuid, image_code]):
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
        redis_cli = get_redis_connection('image_code')
        result = redis_cli.get(uuid)
        redis_cli.delete(uuid)
        if not result:
            return Response({'error': "图片验证码已过期"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if result.lower() != image_code:
            return Response({'error': "图片验证码错误"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

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
    permission_classes = [IsAuthenticated, BasePermission]

    def upload_avatar(self, request, *args, **kwargs):
        """上传用户头像"""
        avatar = request.data.get('avatar')
        if not avatar:
            return Response({'error': '上传失败，文件不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if avatar.size > 1024 * 300:
            return Response({'error': '上传失败，文件大小不能超过300kb'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = request.get_object()
        serializer = self.get_serializer(user, data={"avatar": avatar}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'url': serializer.data['avatar']}, status=status.HTTP_200_OK)

    @staticmethod
    def verify_auth_code(code, mobile):
        """验证短信验证码"""
        if not code:
            return {'error': '验证码不能为空'}
        if not mobile:
            return {'error': '手机号不能为空'}
        redis_cli = get_redis_connection('code')
        result = redis_cli.get(mobile)
        if not result:
            return {'error': '验证码已过期, 请重新获取'}
        elif result != code:
            return {'error': '验证码错误'}
        else:
            redis_cli.delete(mobile)

    def bind_mobile(self, request, *args, **kwargs):
        """绑定手机号"""
        code = request.data.get('code')
        mobile = request.data.get('mobile')
        if result := self.verify_auth_code(code, mobile):
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if Users.objects.filter(mobile=mobile).exists():
            return Response({'error': '手机号已被用户绑定'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = request.user
        user.mobile = mobile
        user.save()
        return Response({'message': "绑定成功"}, status=status.HTTP_200_OK)

    def unbind_mobile(self, request, *args, **kwargs):
        """解绑手机号"""
        code = request.data.get('code')
        mobile = request.data.get('mobile')
        if result := self.verify_auth_code(code, mobile):
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = request.user
        if user.mobile != mobile:
            return Response({'error': '当前用户没有绑定该号码'}, status=status.HTTP_400_BAD_REQUEST)
        user.mobile = ''
        user.save()
        return Response({'message': '解绑成功'}, status=status.HTTP_200_OK)

    def update_nickname(self, request, *args, **kwargs):
        """修改昵称"""
        last_name = request.data.get('last_name')
        if not last_name:
            return Response({'error': '参数不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = self.get_object()
        user.last_name = last_name
        user.save()
        return Response({'message': '修改成功'}, status=status.HTTP_200_OK)

    def update_email(self, request, *args, **kwargs):
        """修改邮箱"""
        email = request.data.get('email')
        if not email:
            return Response({'error': '参数不能为空'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not re.match(r'^([a-zA-Z\d][\w-]{2,})@(\w{2,})\.([a-z]{2,})(\.[a-z]{2,})?$', email):
            return Response({'error': '邮箱格式错误'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user = self.get_object()
        if user.email == email:
            return Response({'error': '此邮箱与绑定邮箱相同'}, status=status.HTTP_400_BAD_REQUEST)
        if Users.objects.filter(email=email).exists():
            return Response({'error': '此邮箱已被绑定'}, status=status.HTTP_400_BAD_REQUEST)
        user.email = email
        user.save()
        return Response({'message': '修改成功'}, status=status.HTTP_200_OK)

    def update_password(self, request, *args, **kwargs):
        """修改密码"""
        code = request.data.get('code')
        mobile = request.data.get('mobile')
        password = request.data.get('password')
        password_confirmation = request.data.get('password_confirmation')
        user = self.get_object()
        if user.mobile != mobile:
            return Response({'error': '此手机号不是该用户绑定号码'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if result := self.verify_auth_code(code, mobile):
            return Response(result, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not password or not password_confirmation:
            return Response({'error': "参数不能为空"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if password != password_confirmation:
            return Response({'error': "两次输入密码不相同"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        user.set_password(password)
        user.save()
        return Response({'message': '修改成功'}, status=status.HTTP_200_OK)


class FileView(APIView):
    """获取头像文件"""

    def get(self, request, name):
        path = settings.MEDIA_ROOT / name
        if os.path.isfile(path):
            return FileResponse(open(path, 'rb'))
        return Response({'error': '没有找到该文件'}, status=status.HTTP_404_NOT_FOUND)


class AddressView(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin,
                  mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    """地址管理视图"""
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated, BasePermission]

    def create(self, request, *args, **kwargs):
        data = request.data
        if data.get('user') != request.user.id:
            return Response({'error': '没有权限进行此操作'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        city = data.get('city')
        if city[-1] == '市':
            data['city'] = city[:-1]
        if not Area.objects.filter(level=1, name=data.get('province'), pid=1).exists():
            return Response({'error': '省份不存在'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        province = Area.objects.get(level=1, name=data.get('province'), pid=1)
        if not Area.objects.filter(level=2, name=data.get('city'), pid=province.id).exists():
            return Response({'error': '城市不存在'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        city = Area.objects.get(level=2, name=data.get('city'), pid=province.id)
        if not Area.objects.filter(level=3, name=data.get('county'), pid=city.id).exists():
            return Response({'error': '区县不存在'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def set_default_address(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.is_default = True
        obj.save()
        queryset = self.get_queryset().filter(user=request.user)
        for item in queryset:
            if item != obj:
                item.is_default = False
                item.save()
        return Response({'message': '设置成功'}, status=status.HTTP_200_OK)


class AreaView(GenericViewSet, mixins.ListModelMixin):
    """省市区县数据查询视图"""
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    filterset_fields = ('level',)


class AdminView(GenericViewSet):
    """管理员视图"""
    queryset = Users.objects.all()
    permission_classes = [IsAuthenticated, AdminPermission]

    def set_vip(self, request, *args, **kwargs):
        """设置VIP"""
        instance = self.get_object()
        instance.is_vip = request.data.get('is_vip')
        instance.save()
        return Response({'message': '设置成功'}, status=status.HTTP_200_OK)
