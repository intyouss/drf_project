from django.urls import path, include, re_path
from .views import IndexView, GoodsView

urlpatterns = [
    # 商城首页接口
    path('index/', IndexView.as_view()),
    # 商品列表接口
    path('goods/', GoodsView.as_view({
        'get': 'list'
    })),
    # 获取单个商品接口
    path('goods/<int:pk>/', GoodsView.as_view({
        'get': 'retrieve'
    }))
]
