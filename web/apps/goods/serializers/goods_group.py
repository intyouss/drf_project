#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/25 11:47
# @File     : goods_group.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import serializers

from ..models import GoodsGroup


class GoodsGroupSerializer(serializers.ModelSerializer):
    """商品分类序列化器"""

    class Meta:
        model = GoodsGroup
        fields = '__all__'
