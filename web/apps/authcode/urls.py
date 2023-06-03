from django.urls import path

from .views import SendSMSView, ImageAuthCodeView

urlpatterns = [
    # 发送短信验证码
    path('smscode/send/', SendSMSView.as_view()),
    # 获取图片验证码
    path('imagecode/<uuid>/', ImageAuthCodeView.as_view())
]
