import os
import json
from alibabacloud_tea_openapi.models import Config
from alibabacloud_dysmsapi20170525.client import Client
from alibabacloud_dysmsapi20170525.models import SendSmsRequest
from alibabacloud_tea_util.models import RuntimeOptions
from django.conf import settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")


class AliYunSMS:
    sign_name = settings.SIGN_NAME
    template_code = settings.TEMPLATE_CODE
    config = Config(
        access_key_id=settings.ACCESS_KEY_ID,
        access_key_secret=settings.ACCESS_KEY_SECRET,
        endpoint=settings.ENDPOINT
    )

    def __init__(self, mobile: str, sms_code: str):
        self.send_sms_request = SendSmsRequest(
            sign_name=self.sign_name,
            template_code=self.template_code,
            phone_numbers=mobile,
            template_param=json.dumps({'code': sms_code})
        )

    def send_msg(self):
        client = Client(self.config)
        runtime = RuntimeOptions()
        try:
            res = client.send_sms_with_options(self.send_sms_request, runtime)
            if res.body.code == 'OK':
                return {'code': 'YES', 'message': "短信发送成功"}
            else:
                return {'code': 'NO', 'error': res.body.message}
        except Exception as e:
            return {'code': 'NO', 'error': '短信发送失败'}