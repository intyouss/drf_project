from django.urls import path

from .views import IndexView, GoodsView, CollectView, GoodsGroupView, GoodsSupplierView

urlpatterns = [
    # 商城首页接口
    path('index/', IndexView.as_view()),
    # 商品列表接口
    path('', GoodsView.as_view({
        'get': 'list'
    })),
    # 获取单个商品接口
    path('<int:pk>/', GoodsView.as_view({
        'get': 'retrieve'
    })),
    path('collect/', CollectView.as_view({
        # 收藏商品
        "post": 'create',
        # 获取收藏商品
        'get': 'list'
    })),
    # 取消收藏
    path('collect/<int:pk>/', CollectView.as_view({
        "delete": 'destroy'
    })),
    # 获取商品分类
    path('group/', GoodsGroupView.as_view({
        'get': 'list'
    })),
    path('admin/supplier/', GoodsSupplierView.as_view({
        'get': 'list',
        'post': 'create'
    }))
]
