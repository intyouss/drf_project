#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/28 11:43
# @File     : cart.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import serializers

from ..models import Cart


class CartSerializer(serializers.ModelSerializer):
    """购物车序列化器"""

    class Meta:
        model = Cart
        fields = '__all__'