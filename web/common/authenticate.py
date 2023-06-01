#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/22 13:08
# @File     : authenticate.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss

from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework import serializers
from users.models import Users


class MyBackend(ModelBackend):
    """
    自定义登录认证类
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = Users.objects.get(Q(username=username) | Q(mobile=username) | Q(email=username))
        except Users.DoseNotExist:
            raise serializers.ValidationError({'error': '未找到用户'})
        else:
            if user.check_password(password):
                return user
            else:
                raise serializers.ValidationError({"error": "密码错误！"})