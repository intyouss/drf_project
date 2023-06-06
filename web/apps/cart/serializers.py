#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/6/6 17:24
# @File     : serializers.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import serializers

from .models import Cart
from goods.serializers import GoodsSerializer


class CartSerializer(serializers.ModelSerializer):
    """写入：购物车序列化器"""

    class Meta:
        model = Cart
        fields = '__all__'


class ReadCartSerializer(serializers.ModelSerializer):
    """读取：购物车序列化器"""
    goods = GoodsSerializer()

    class Meta:
        model = Cart
        fields = '__all__'


class CartInfoSerializer(serializers.ModelSerializer):
    """购物车商品详情序列化器"""
    goods = GoodsSerializer()

    class Meta:
        model = Cart
        fields = '__all__'