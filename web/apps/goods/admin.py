from django.contrib import admin
from .models import GoodsGroup, Goods, GoodsCarousel, Detail, Collect


@admin.register(GoodsGroup)
class GoodsGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_status']


@admin.register(Goods)
class GoodsGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'price', 'stock', 'sales', 'is_on']


@admin.register(Detail)
class GoodsGroupAdmin(admin.ModelAdmin):
    list_display = ['goods', 'producer', 'norms']


@admin.register(GoodsCarousel)
class GoodsGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_status']


@admin.register(Collect)
class GoodsGroupAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods']