from django.urls import path

from .views import OrderView, OrderCommentView, OrderPayView

urlpatterns = [
    # 提交订单
    path('submit/', OrderView.as_view({
        'post': 'create'
    })),
    # 获取订单列表
    path('', OrderView.as_view({
        'get': 'list'
    })),
    # 获取单个订单
    path('<int:pk>/', OrderView.as_view({
        'get': 'retrieve'
    })),
    # 关闭订单
    path('<int:pk>/close/', OrderView.as_view({
        'put': 'close_order'
    })),
    path('comment/', OrderCommentView.as_view({
        # 评论订单
        'post': 'create',
        # 获取订单评论
        'get': 'list'
    })),
    # 订单支付会员检查
    path('check/', OrderPayView.as_view({
        'post': 'check'
    })),
    # 支付宝支付界面获取
    path('ali/pay/', OrderPayView.as_view({
        'post': 'ali_pay'
    })),
    # 会员卡直接支付
    path('club/pay/', OrderPayView.as_view({
        'post': 'club_pay'
    }))
]
