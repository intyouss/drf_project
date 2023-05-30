from django.contrib import admin

from .models import Order, OrderGoods, OrderCommit


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'order_number', 'amount', 'address', 'pay_type', 'status']


@admin.register(OrderGoods)
class OrderGoodsAdmin(admin.ModelAdmin):
    list_display = ['order', 'goods', 'price', 'number']


@admin.register(OrderCommit)
class OrderCommitAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods', 'order', 'content', 'star', 'rate']