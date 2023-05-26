#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/25 11:42
# @File     : goods.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import serializers

from ..models import Goods


class GoodsSerializer(serializers.ModelSerializer):
    """商品序列化器"""

    class Meta:
        model = Goods
        exclude = ('updated_time', 'created_time',)