from django.urls import path, include, re_path
from .views import IndexView

urlpatterns = [
    path('index/', IndexView.as_view())
]
