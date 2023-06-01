#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/22 17:16
# @File     : address.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss

from rest_framework import serializers
from ..models import Area


class AreaSerializer(serializers.ModelSerializer):
    """地区数据模型序列化器"""

    class Meta:
        model = Area
        fields = '__all__'