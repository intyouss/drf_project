import time

from django.db import models
from django.db.models import Manager

from common.default_model import BaseModel


class Order(BaseModel):
    """订单表"""
    STATUS = (
        (1, '待支付'),
        (2, '待发货'),
        (3, '配送中'),
        (4, '待评价'),
        (5, '已完成'),
        (6, '已关闭')
    )
    PAY_TYPE = (
        (1, '支付宝'),
        (2, '微信')
    )

    user = models.ForeignKey('users.Users', verbose_name='下单用户', on_delete=models.CASCADE)
    order_number = models.CharField(max_length=200, verbose_name='订单单号')
    amount = models.FloatField(verbose_name='总金额')
    address = models.CharField(verbose_name='收货地址', max_length=200)
    status = models.SmallIntegerField(choices=STATUS, verbose_name='订单状态', default=1)
    pay_time = models.DateTimeField(verbose_name='支付时间', blank=True, null=True)
    pay_type = models.SmallIntegerField(choices=PAY_TYPE, verbose_name='支付方式', blank=True, null=True)
    trade_number = models.CharField(verbose_name='支付单号', max_length=50, blank=True, null=True)

    objects = Manager()

    class Meta:
        db_table = 'order'
        verbose_name = '订单表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.order_number

    def set_order_number(self):
        self.order_number = str(int(time.time())) + str(self.user.id)


class OrderGoods(BaseModel):
    """订单商品表"""
    order = models.ForeignKey('Order', verbose_name='所属订单', on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.Goods', verbose_name='商品', on_delete=models.CASCADE)
    price = models.FloatField(verbose_name='商品价格')
    number = models.IntegerField(verbose_name='商品数量', default=1)

    objects = Manager()

    class Meta:
        db_table = 'order_goods'
        verbose_name = '订单商品表'
        verbose_name_plural = verbose_name


class OrderComment(BaseModel):
    """订单商品评论表"""
    LEVEL = (
        (1, '好评'),
        (2, '中评'),
        (3, '差评')
    )
    STAR = (
        (1, '一星'),
        (2, '二星'),
        (3, '三星'),
        (4, '四星'),
        (5, '五星')
    )

    user = models.ForeignKey('users.Users', verbose_name='评论的用户', on_delete=models.CASCADE)
    goods = models.ForeignKey('goods.Goods', verbose_name='商品ID', on_delete=models.CASCADE)
    order = models.ForeignKey('Order', verbose_name='所属订单', on_delete=models.CASCADE)
    content = models.CharField(max_length=255, verbose_name='评论的内容', default='')
    rate = models.SmallIntegerField(choices=LEVEL, default=1, verbose_name='评论等级', blank=True)
    star = models.SmallIntegerField(choices=STAR, verbose_name='评论星级', default=5, blank=True)

    objects = Manager()

    class Meta:
        db_table = 'order_comment'
        verbose_name = '订单商品评论表'
        verbose_name_plural = verbose_name
