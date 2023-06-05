from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Manager

from common.default_model import BaseModel


class Users(AbstractUser, BaseModel):
    """用户表"""
    mobile = models.CharField(max_length=11, default='', verbose_name='手机号码')
    avatar = models.ImageField(verbose_name='用户头像', blank=True, null=True)
    is_vip = models.BooleanField(verbose_name='是否为贵宾身份', default=False)

    class Meta:
        db_table = 'users'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name


class Address(models.Model):
    """收货地址表"""
    user = models.ForeignKey('Users', verbose_name='用户名', on_delete=models.CASCADE)
    phone = models.CharField(verbose_name='手机号码', max_length=11)
    name = models.CharField(verbose_name='联系人', max_length=20)
    province = models.CharField(verbose_name='省份', max_length=20)
    city = models.CharField(verbose_name='城市', max_length=20)
    county = models.CharField(verbose_name='区县', max_length=20)
    address = models.CharField(verbose_name='详细地址', max_length=256)
    is_default = models.BooleanField(verbose_name='是否为默认地址', default=False)

    objects = Manager()

    class Meta:
        db_table = 'users_address'
        verbose_name = '收货地址表'
        verbose_name_plural = verbose_name


class Area(models.Model):
    """
    省市县区域表
    """
    level_choice = (
        (0, '国家'),
        (1, '省份'),
        (2, '市'),
        (3, '区/县')
    )
    pid = models.IntegerField(verbose_name='上级ID')
    name = models.CharField(max_length=32, verbose_name='地区名')
    level = models.IntegerField(choices=level_choice, verbose_name='区域等级')

    objects = Manager()

    class Meta:
        db_table = 'users_area'
        verbose_name = '地区表'
        verbose_name_plural = verbose_name
