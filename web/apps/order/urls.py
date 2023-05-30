from django.urls import path, include, re_path

from .views import OrderView

urlpatterns = [
    path('submit/', OrderView.as_view({
        'post': 'create'
    }))
]
