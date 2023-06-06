#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/25 11:45
# @File     : goods_carousel.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import serializers

from ..models import GoodsCarousel


class GoodsCarouselSerializer(serializers.ModelSerializer):
    """商品轮播图序列化器"""

    class Meta:
        model = GoodsCarousel
        fields = '__all__'
