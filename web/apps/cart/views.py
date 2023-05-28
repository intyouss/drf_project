from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Cart
from .serializers.cart import CartSerializer


class CartView(GenericViewSet, mixins.CreateModelMixin,
               mixins.RetrieveModelMixin,
               mixins.UpdateModelMixin,
               mixins.DestroyModelMixin,
               mixins.ListModelMixin):
    """添加购物车商品视图"""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        goods = request.data.get('goods')
        if Cart.objects.filter(user=user, goods=goods).exist():
            cart_goods = Cart.objects.get(user=user, goods=goods)
            cart_goods.number += 1
            cart_goods.save()
            serializer = self.get_serializer(cart_goods)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        request.data['user'] = user.id
        return super().create(request, *args, **kwargs)
