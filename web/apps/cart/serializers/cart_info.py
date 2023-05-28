#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/28 11:43
# @File     : cart_info.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import serializers

from ..models import Cart
from apps.goods.serializers.goods import GoodsSerializer


class CartInfoSerializer(serializers.ModelSerializer):
    """购物车商品详情序列化器"""
    goods = GoodsSerializer()

    class Meta:
        model = Cart
        fields = '__all__'