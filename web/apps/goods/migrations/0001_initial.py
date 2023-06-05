# Generated by Django 4.2.1 on 2023-06-05 22:52

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsCarousel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(default='', max_length=32, verbose_name='轮播图名称')),
                ('image', models.ImageField(blank=True, max_length=256, null=True, upload_to='', verbose_name='轮播图')),
                ('is_status', models.BooleanField(blank=True, default=False, verbose_name='是否启用')),
                ('seq', models.IntegerField(blank=True, default=1, verbose_name='顺序')),
            ],
            options={
                'verbose_name': '商品轮播图表',
                'verbose_name_plural': '商品轮播图表',
                'db_table': 'goods_carousel',
            },
        ),
        migrations.CreateModel(
            name='GoodsGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, verbose_name='名称')),
                ('image', models.ImageField(blank=True, max_length=20, null=True, upload_to='', verbose_name='分类图标')),
                ('is_status', models.BooleanField(default=True, verbose_name='是否启用')),
            ],
            options={
                'verbose_name': '商品分类表',
                'verbose_name_plural': '商品分类表',
                'db_table': 'goods_group',
            },
        ),
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(blank=True, max_length=200, null=True, verbose_name='商家名')),
                ('telephone', models.CharField(blank=True, max_length=16, null=True, verbose_name='电话')),
                ('linker', models.CharField(blank=True, max_length=20, null=True, verbose_name='联系人')),
                ('office', models.CharField(blank=True, max_length=20, null=True, verbose_name='职务')),
                ('desc', models.CharField(blank=True, max_length=256, null=True, verbose_name='商家描述')),
            ],
            options={
                'verbose_name': '供应商表',
                'verbose_name_plural': '供应商表',
                'db_table': 'goods_supplier',
            },
        ),
        migrations.CreateModel(
            name='Goods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(default='', max_length=200, verbose_name='商品名')),
                ('desc', models.CharField(max_length=256, verbose_name='商品描述')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='商品价格')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='封面图')),
                ('stock', models.IntegerField(blank=True, default=1, verbose_name='库存')),
                ('sales', models.IntegerField(blank=True, default=0, verbose_name='销量')),
                ('is_on', models.BooleanField(blank=True, default=False, verbose_name='是否上架')),
                ('is_recommend', models.BooleanField(blank=True, default=False, verbose_name='是否推荐')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodsgroup', verbose_name='商品类别')),
            ],
            options={
                'verbose_name': '商品表',
                'verbose_name_plural': '商品表',
                'db_table': 'goods',
            },
        ),
        migrations.CreateModel(
            name='Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('producer', models.CharField(max_length=200, verbose_name='厂商')),
                ('norms', models.CharField(max_length=200, verbose_name='规格')),
                ('details', ckeditor.fields.RichTextField(blank=True, verbose_name='商品详情')),
                ('goods', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='goods.goods', verbose_name='商品')),
            ],
            options={
                'verbose_name': '商品详情表',
                'verbose_name_plural': '商品详情表',
                'db_table': 'goods_detail',
            },
        ),
        migrations.CreateModel(
            name='Collect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goods', verbose_name='商品ID')),
                ('user', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户ID')),
            ],
            options={
                'verbose_name': '收藏商品表',
                'verbose_name_plural': '收藏商品表',
                'db_table': 'goods_collect',
            },
        ),
    ]
