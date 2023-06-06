from django.urls import path

from .views import IndexView, GoodsView, CollectView, GoodsGroupView, GoodsSupplierView, GoodsStockView

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
    # 获取供应商信息及添加供应商
    path('admin/supplier/', GoodsSupplierView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    # 获取单一供应商，删除，更新
    path('admin/supplier/<int:pk>', GoodsSupplierView.as_view({
        'put': 'update',
        'delete': 'destroy',
        'get': 'retrieve'
    })),
    # 获取商品入库信息及添加入库账单
    path('admin/stock/', GoodsStockView.as_view({
        'get': 'list',
        'post': 'create'
    })),
    # 获取单一供应商，删除
    path('admin/stock/<int:pk>', GoodsStockView.as_view({
        'delete': 'destroy',
        'get': 'retrieve'
    }))
]
