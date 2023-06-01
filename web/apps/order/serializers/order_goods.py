#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/25 11:49
# @File     : cart.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from goods.serializers.goods import GoodsSerializer
from rest_framework import serializers

from ..models import OrderGoods


class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单商品序列化器"""
    goods = GoodsSerializer()

    class Meta:
        model = OrderGoods
        fields = ('goods', 'number', 'price')
