from django.contrib import admin
from .models import GoodsGroup, Goods, GoodsCarousel, Detail, Collect


@admin.register(GoodsGroup)
class GoodsGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_status']


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'price', 'stock', 'sales', 'is_on']


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['goods', 'producer', 'norms']


@admin.register(GoodsCarousel)
class GoodsCarouselAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_status']


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods']