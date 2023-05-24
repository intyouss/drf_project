#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/22 14:11
# @File     : users.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss

from rest_framework import serializers

from ..models import Users


class UserSerializer(serializers.ModelSerializer):
    """
    用户模型序列化器
    """
    class Meta:
        model = Users
        fields = ['id', 'username', 'last_name', 'email', 'mobile', 'avatar']