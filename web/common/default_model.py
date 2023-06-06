#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/5/21 18:07
# @File     : default_model.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss

from django.db import models


class BaseModel(models.Model):
    """
    公共字段模型(抽象模型)
    """
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        abstract = True
