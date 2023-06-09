#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/6/6 17:26
# @File     : serializers.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import serializers

from .models import Address, Area, Users


class AddressSerializer(serializers.ModelSerializer):
    """收货地址模型序列化器"""

    class Meta:
        model = Address
        fields = '__all__'


class AreaSerializer(serializers.ModelSerializer):
    """地区数据模型序列化器"""

    class Meta:
        model = Area
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    用户模型序列化器
    """

    class Meta:
        model = Users
        fields = ['id', 'username', 'last_name', 'email', 'mobile', 'avatar']