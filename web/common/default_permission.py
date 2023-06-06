#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/6/6 17:28
# @File     : default_permission.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import permissions


class BasePermission(permissions.BasePermission):
    """基础权限限制"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return obj.user == request.user


class AdminPermission(BasePermission):
    """管理员权限限制"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False