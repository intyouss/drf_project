from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Manager

from common.default_model import BaseModel


class Users(AbstractUser, BaseModel):
    """用户表"""
    mobile = models.CharField(max_length=11, default='', verbose_name='手机号码')
    avatar = models.ImageField(verbose_name='用户头像', blank=True, null=True)

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

    def merge_address(self):
        address_str = '{}{}{}{} {} {}'.format(
            self.province,
            self.city,
            self.county,
            self.address,
            self.name,
            self.phone
        )
        return address_str


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


class ClubCard(BaseModel):
    """
    会员卡表
    """
    def auto_sort():
        # 方法必须放在字段前面
        count = ClubCard.objects.count()
        return '1000000001' if (count is None) else str(count + 1000000001)
    card_number = models.CharField(verbose_name='卡号', auto_created=True, default=auto_sort, max_length=11)
    user = models.ForeignKey('Users', verbose_name='用户', on_delete=models.CASCADE, related_name='vip')
    money = models.FloatField(verbose_name='余额')

    objects = Manager()

    class Meta:
        db_table = 'users_club_card'
        verbose_name = '会员卡表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.card_number