#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/25 11:49
# @File     : cart.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import serializers

from ..models import Order, OrderComment


class OrderCommentSerializer(serializers.ModelSerializer):
    """订单评论序列化器"""

    class Meta:
        model = OrderComment
        fields = '__all__'