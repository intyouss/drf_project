from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from .views import LoginView, RegisterView, UserView, AddressView, SendSMSView, AreaView, ImageAuthCodeView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    # 刷新Token
    path('token/refresh/', TokenRefreshView.as_view()),
    # 校验Token
    path('token/verify/', TokenVerifyView.as_view()),
    # 获取单个用户信息路由
    path('<int:pk>/', UserView.as_view({'get': 'retrieve'})),
    # 上传头像路由
    path('<int:pk>/avatar/upload/', UserView.as_view({'post': 'upload_avatar'})),
    # 添加地址和获取地址列表的路由
    path('address/', AddressView.as_view({
        'post': "create",
        'get': 'list'
    })),
    # 修改地址和删除地址列表的路由
    path('address/<int:pk>/', AddressView.as_view({
        'delete': "destroy",
        'put': 'update'
    })),
    # 设置默认地址
    path('address/<int:pk>/default/', AddressView.as_view({
        'put': 'set_default_address'
    })),
    # 发送短信验证码
    path('sms/send/', SendSMSView.as_view()),
    # 绑定手机号
    path('<int:pk>/mobile/bind/', UserView.as_view({
        'put': 'bind_mobile'
    })),
    # 解绑手机号
    path('<int:pk>/mobile/unbind/', UserView.as_view({
        'put': 'unbind_mobile'
    })),
    # 修改昵称
    path('<int:pk>/nickname/update/', UserView.as_view({
        'put': 'update_nickname'
    })),
    # 修改邮箱
    path('<int:pk>/email/update/', UserView.as_view({
        'put': 'update_email'
    })),
    # 修改密码
    path('<int:pk>/password/update/', UserView.as_view({
        'put': 'update_password'
    })),
    # 查询省市区县数据
    path('area/', AreaView.as_view({
        'get': 'list'
    })),
    # 获取图片验证码
    path('imagecode/<uuid>/', ImageAuthCodeView.as_view())
]
