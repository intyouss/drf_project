# Generated by Django 4.2.1 on 2023-06-05 22:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('order_number', models.CharField(max_length=200, verbose_name='订单单号')),
                ('amount', models.FloatField(verbose_name='总金额')),
                ('address', models.CharField(max_length=200, verbose_name='收货地址')),
                ('status', models.SmallIntegerField(choices=[(1, '待支付'), (2, '待发货'), (3, '配送中'), (4, '待评价'), (5, '已完成'), (6, '已关闭')], default=1, verbose_name='订单状态')),
                ('pay_time', models.DateTimeField(blank=True, null=True, verbose_name='支付时间')),
                ('pay_type', models.SmallIntegerField(blank=True, choices=[(1, '支付宝'), (2, '微信')], null=True, verbose_name='支付方式')),
                ('trade_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='支付单号')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='下单用户')),
            ],
            options={
                'verbose_name': '订单表',
                'verbose_name_plural': '订单表',
                'db_table': 'order',
            },
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('price', models.FloatField(verbose_name='商品价格')),
                ('number', models.IntegerField(default=1, verbose_name='商品数量')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goods', verbose_name='商品')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order', verbose_name='所属订单')),
            ],
            options={
                'verbose_name': '订单商品表',
                'verbose_name_plural': '订单商品表',
                'db_table': 'order_goods',
            },
        ),
        migrations.CreateModel(
            name='OrderComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('updated_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('content', models.CharField(default='', max_length=255, verbose_name='评论的内容')),
                ('rate', models.SmallIntegerField(blank=True, choices=[(1, '好评'), (2, '中评'), (3, '差评')], default=1, verbose_name='评论等级')),
                ('star', models.SmallIntegerField(blank=True, choices=[(1, '一星'), (2, '二星'), (3, '三星'), (4, '四星'), (5, '五星')], default=5, verbose_name='评论星级')),
                ('goods', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goods', verbose_name='商品ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order', verbose_name='所属订单')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论的用户')),
            ],
            options={
                'verbose_name': '订单商品评论表',
                'verbose_name_plural': '订单商品评论表',
                'db_table': 'order_comment',
            },
        ),
    ]
