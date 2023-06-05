#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/22 18:15
# @File     : order.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from rest_framework import permissions


class AdminPermission(permissions.BasePermission):
    """管理员权限管控"""

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False
