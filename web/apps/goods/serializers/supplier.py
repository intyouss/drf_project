#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/25 11:48
# @File     : detail.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import serializers

from ..models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    """商品供应商序列化器"""

    class Meta:
        model = Supplier
        fields = '__all__'