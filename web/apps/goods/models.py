from ckeditor.fields import RichTextField
from django.db import models
from common.default_model import BaseModel


class Goods(BaseModel):
    """商品表"""
    group = models.ForeignKey('GoodsGroup', verbose_name='商品类别', on_delete=models.CASCADE())
    name = models.CharField(verbose_name='商品名', max_length=20)
    desc = models.CharField(verbose_name='商品描述', max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='价格')
    image = models.ImageField(verbose_name='封面图连接', blank=True, null=True)
    stock = models.IntegerField(default=1, verbose_name='库存')
    sales = models.IntegerField(default=0, verbose_name='销量')
    is_on = models.BooleanField(default=False, verbose_name='是否上架')
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐')

    class Meta:
        db_table = 'goods'
        verbose_name = '商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsGroup(models.Model):
    """商品分类表"""
    name = models.CharField(max_length=20, verbose_name='名称')
    image = models.ImageField(max_length=20, verbose_name='分类图标')
    status = models.BooleanField(verbose_name='是否启用')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'goods_group'
        verbose_name = '商品分类表'
        verbose_name_plural = verbose_name


class Detail(BaseModel):
    """商品详情表"""
    goods = models.OneToOneField('Goods', verbose_name='商品', on_delete=models.CASCADE())
    producer = models.CharField(verbose_name='厂商', max_length=200)
    norms = models.CharField(verbose_name='规格', max_length=200)
    details = RichTextField(blank=True, verbose_name='商品详情')

    class Meta:
        db_table = 'detail'
        verbose_name = '商品详情表'
        verbose_name_plural = verbose_name


class GoodsCarousel(BaseModel):
    """商品轮播图表"""
    name = models.CharField(verbose_name='轮播图名称', max_length=32)
    image = models.ImageField(verbose_name='轮播图链接', max_length=256)
    url = models.CharField(verbose_name='跳转地址', max_length=256)
    is_status = models.BooleanField(verbose_name='是否启用')
    seq = models.IntegerField(verbose_name='顺序', default=1)

    class Meta:
        db_table = 'goods_carousel'
        verbose_name = '商品轮播图表'
        verbose_name_plural = verbose_name

