from django.contrib import admin
from django.urls import path, include, re_path

from .views import CartView

urlpatterns = [
    # 添加购物车商品
    path('goods/', CartView.as_view({
        'post': 'create'
    }))
]
