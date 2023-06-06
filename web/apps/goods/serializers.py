#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/6/6 17:21
# @File     : serializers.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import serializers

from .models import Collect, Detail, Goods, GoodsCarousel, GoodsGroup, StockInfo, Supplier


class CollectSerializer(serializers.ModelSerializer):
    """收藏商品序列化器"""

    class Meta:
        model = Collect
        fields = '__all__'


class DetailSerializer(serializers.ModelSerializer):
    """商品详情序列化器"""

    class Meta:
        model = Detail
        fields = ['producer', "norms", "details"]


class GoodsCarouselSerializer(serializers.ModelSerializer):
    """商品轮播图序列化器"""

    class Meta:
        model = GoodsCarousel
        fields = '__all__'


class GoodsGroupSerializer(serializers.ModelSerializer):
    """商品分类序列化器"""

    class Meta:
        model = GoodsGroup
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    """商品序列化器"""
    group = GoodsGroupSerializer()

    class Meta:
        model = Goods
        exclude = ('updated_time', 'created_time',)


class StockInfoSerializer(serializers.ModelSerializer):
    """商品供应商序列化器"""

    class Meta:
        model = StockInfo
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    """商品供应商序列化器"""

    class Meta:
        model = Supplier
        fields = '__all__'