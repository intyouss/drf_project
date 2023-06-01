from django.urls import path

from .views import CartView

urlpatterns = [
    # 添加购物车商品
    path('goods/', CartView.as_view({
        'post': 'create',
        'get': 'list'
    })),
    # 修改商品选中状态
    path('goods/<int:pk>/checked/', CartView.as_view({
        'put': 'update_goods_status'
    })),
    # 修改商品数量
    path('goods/<int:pk>/number/', CartView.as_view({
        'put': 'update_goods_number'
    })),
    # 删除商品
    path('goods/<int:pk>/delete/', CartView.as_view({
        'delete': 'destroy'
    }))
]
