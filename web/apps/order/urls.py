from django.urls import path, include, re_path

from .views import OrderView, OrderCommentView

urlpatterns = [
    path('submit/', OrderView.as_view({
        'post': 'create'
    })),
    path('', OrderView.as_view({
        'get': 'list'
    })),
    path('<int:pk>/', OrderView.as_view({
        'get': 'retrieve'
    })),
    path('<int:pk>/close/', OrderView.as_view({
        'put': 'close_order'
    })),
    path('comment/', OrderCommentView.as_view({
        'post': 'create',
        'get': 'list'
    }))
]
