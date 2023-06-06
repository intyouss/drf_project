from django.contrib import admin

from .models import GoodsGroup, Goods, GoodsCarousel, Detail, Collect, Supplier, StockInfo


@admin.register(GoodsGroup)
class GoodsGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_status']


@admin.register(Goods)
class GoodsAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'price', 'stock', 'sales', 'is_on']


@admin.register(Detail)
class DetailAdmin(admin.ModelAdmin):
    list_display = ['goods', 'get_producer', 'norms']

    def get_producer(self, obj):
        return ','.join([str(tag) for tag in obj.producer.all()])

    get_producer.short_description = '供应商'


@admin.register(GoodsCarousel)
class GoodsCarouselAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_status']


@admin.register(Collect)
class CollectAdmin(admin.ModelAdmin):
    list_display = ['user', 'goods']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'telephone', 'linker', 'office', 'desc']


@admin.register(StockInfo)
class StockInfoAdmin(admin.ModelAdmin):
    list_display = ['goods', 'producer', 'admin', 'price', 'number', 'mark', 'created_time']