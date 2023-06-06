from django.db import models
from django.db.models import Manager

from common.default_model import BaseModel


class Cart(BaseModel):
    """购物车商品表"""
    user = models.ForeignKey('users.Users', verbose_name='用户', on_delete=models.CASCADE, blank=True)
    goods = models.ForeignKey('goods.Goods', verbose_name='商品', on_delete=models.CASCADE)
    number = models.SmallIntegerField(verbose_name='商品数量', default=1, blank=True)
    is_checked = models.BooleanField(verbose_name='是否选中', default=True, blank=True)

    objects = Manager()

    class Meta:
        db_table = 'cart'
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
