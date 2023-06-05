#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/6/5 18:12
# @File     : supplier.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss

from rest_framework import permissions


class SupplierPermission(permissions.BasePermission):
    """供应商详情权限限制"""
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False