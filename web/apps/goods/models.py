from ckeditor.fields import RichTextField
from django.db import models
from django.db.models import Manager

from common.default_model import BaseModel


class Goods(BaseModel):
    """商品表"""
    group = models.ForeignKey('GoodsGroup', verbose_name='商品类别', on_delete=models.CASCADE)
    name = models.CharField(verbose_name='商品名', max_length=200, default='')
    desc = models.CharField(verbose_name='商品描述', max_length=256)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品价格')
    image = models.ImageField(verbose_name='封面图', blank=True, null=True)
    stock = models.IntegerField(default=1, verbose_name='库存', blank=True)
    sales = models.IntegerField(default=0, verbose_name='销量', blank=True)
    is_on = models.BooleanField(default=False, verbose_name='是否上架', blank=True)
    is_recommend = models.BooleanField(default=False, verbose_name='是否推荐', blank=True)

    objects = Manager()

    class Meta:
        db_table = 'goods'
        verbose_name = '商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsGroup(models.Model):
    """商品分类表"""
    name = models.CharField(max_length=20, verbose_name='名称')
    image = models.ImageField(max_length=20, verbose_name='分类图标', blank=True, null=True)
    is_status = models.BooleanField(verbose_name='是否启用', default=True)

    objects = Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'goods_group'
        verbose_name = '商品分类表'
        verbose_name_plural = verbose_name


class Detail(BaseModel):
    """商品详情表"""
    goods = models.OneToOneField('Goods', verbose_name='商品', on_delete=models.CASCADE)
    producer = models.ManyToManyField('Supplier', verbose_name='供应商', related_name='goods', blank=True)
    norms = models.CharField(verbose_name='规格', max_length=200)
    details = RichTextField(blank=True, verbose_name='商品详情')

    objects = Manager()

    class Meta:
        db_table = 'goods_detail'
        verbose_name = '商品详情表'
        verbose_name_plural = verbose_name


class GoodsCarousel(BaseModel):
    """商品轮播图表"""
    name = models.CharField(verbose_name='轮播图名称', max_length=32, default='')
    image = models.ImageField(verbose_name='轮播图', max_length=256, blank=True, null=True)
    is_status = models.BooleanField(verbose_name='是否启用', default=False, blank=True)
    seq = models.IntegerField(verbose_name='顺序', default=1, blank=True)
    objects = Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'goods_carousel'
        verbose_name = '商品轮播图表'
        verbose_name_plural = verbose_name


class Collect(models.Model):
    """收藏商品表"""
    user = models.ForeignKey('users.Users', verbose_name='用户ID', on_delete=models.CASCADE, blank=True)
    goods = models.ForeignKey('Goods', verbose_name='商品ID', on_delete=models.CASCADE)

    objects = Manager()

    class Meta:
        db_table = 'goods_collect'
        verbose_name = '收藏商品表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods


class Supplier(BaseModel):
    """供应商表"""
    name = models.CharField(verbose_name='商家名', max_length=200, blank=True, null=True)
    telephone = models.CharField(verbose_name='电话', max_length=16, blank=True, null=True)
    linker = models.CharField(verbose_name='联系人', max_length=20, blank=True, null=True)
    office = models.CharField(verbose_name='职务', max_length=20, blank=True, null=True)
    desc = models.CharField(verbose_name='商家描述', max_length=256, blank=True, null=True)

    objects = Manager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'goods_supplier'
        verbose_name = '供应商表'
        verbose_name_plural = verbose_name
