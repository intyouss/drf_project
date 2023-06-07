#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : intyou
# @Time     : 2023/6/7 13:40
# @File     : celery.py
# @Email    : intyou@outlook.com
# @GitHub   : https://github.com/intyouss
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# 设置Django项目的默认设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')

# 创建Celery实例
app = Celery('web')

# 使用Django的设置模块配置Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)