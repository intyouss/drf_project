import re
import random

from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from common.logs import logger
from common.sms import AliYunSMS
from libs.captcha.captcha import captcha


class ImageAuthCodeView(APIView):
    """图片验证码视图"""
    throttle_classes = (AnonRateThrottle,)  # 限制访问频率

    def get(self, request, uuid):
        text, image = captcha.generate_captcha()
        redis_cli = get_redis_connection('image_code')
        redis_cli.setex(uuid, 100, text)
        logger.info('图片验证码发送成功')
        return HttpResponse(image, content_type='image/jpeg')


class SendSMSView(APIView):
    """短信验证码"""

    throttle_classes = (AnonRateThrottle,)

    def post(self, request):
        mobile = request.data.get('mobile')
        res = re.match(r"^1(3[0-9]|5[0-3,5-9]|7[1-3,5-8]|8[0-9])\d{8}$", mobile)
        if not res:
            logger.error('无效的手机号码')
            return Response({'error': '无效的手机号码'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        code = self.get_random_code()
        result = AliYunSMS(mobile=mobile, sms_code=code).send_msg()
        if result['code'] == 'YES':
            redis_cli = get_redis_connection('code')
            redis_cli.setex(mobile, 500, code)
            logger.info('短信验证码发送成功')
            return Response(result, status=status.HTTP_200_OK)
        else:
            logger.error('短信验证码发送失败')
            return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @staticmethod
    def get_random_code():
        return ''.join(random.sample('0123456789', 6))
