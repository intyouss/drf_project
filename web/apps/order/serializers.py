#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/6/6 17:18
# @File     : serializers.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import serializers

from .models import Order, OrderComment, OrderGoods
from goods.serializers.goods import GoodsSerializer


class OrderSerializer(serializers.ModelSerializer):
    """订单序列化器"""

    class Meta:
        model = Order
        fields = '__all__'


class OrderCommentSerializer(serializers.ModelSerializer):
    """订单评论序列化器"""

    class Meta:
        model = OrderComment
        fields = '__all__'


class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单商品序列化器"""
    goods = GoodsSerializer()

    class Meta:
        model = OrderGoods
        fields = ('goods', 'number', 'price')