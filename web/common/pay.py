#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/6/1 10:37
# @File     : pay.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
import os

from alipay import AliPay
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")


class ALiPay:
    # 密钥
    public_key = open(settings.PUBLIC_KEY).read()
    private_key = open(settings.PRIVATE_KEY).read()
    gateway = settings.ALIPAY_GATEWAY + '?'
    app_id = settings.APP_ID
    return_url = None
    notify_url = None

    def __init__(self):
        # 初始化支付对象
        self.pay_obj = AliPay(
            appid=self.app_id,
            app_private_key_string=self.private_key,
            alipay_public_key_string=self.public_key,
            debug=True,
        )

    def mobile_payment_url(self, order_number, amount, title):
        """生成手机应用的支付地址"""
        url = self.pay_obj.api_alipay_trade_wap_pay(
            subject=title,
            out_trade_no=order_number,
            total_amount=amount,
            return_url=self.return_url,
            notify_url=self.notify_url,
        )
        pay_url = self.gateway + url
        return pay_url