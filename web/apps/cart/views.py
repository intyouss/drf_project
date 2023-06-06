from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from common.default_permission import BasePermission
from .models import Cart
from .serializers import CartSerializer, ReadCartSerializer


class CartView(GenericViewSet, mixins.CreateModelMixin,
               mixins.UpdateModelMixin, mixins.DestroyModelMixin
               ):
    """添加购物车商品视图"""
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, BasePermission]

    def get_serializer_class(self):
        """读写分离"""
        if self.action == 'list':
            return ReadCartSerializer
        else:
            return self.serializer_class

    def create(self, request, *args, **kwargs):
        user = request.user
        goods = request.data.get('goods')
        if Cart.objects.filter(user=user, goods=goods).exists():
            cart_goods = Cart.objects.get(user=user, goods=goods)
            cart_goods.number += 1
            cart_goods.save()
            serializer = self.get_serializer(cart_goods)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        request.data['user'] = user.id
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def update_goods_status(self, request, *args, **kwargs):
        """修改商品的选中状态"""
        obj = self.get_object()
        obj.is_checked = not obj.is_checked
        obj.save()
        return Response({'message': '修改成功'}, status=status.HTTP_200_OK)

    def update_goods_number(self, request, *args, **kwarg):
        """修改商品数量"""
        number = request.data.get('number')
        if not isinstance(number, int):
            return Response({'error': '参数不能为空！'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        obj = self.get_object()
        stock = obj.goods.stock
        if number <= 0:
            obj.delete()
        elif number > stock:
            obj.number = stock
            obj.save()
        else:
            obj.number = number
            obj.save()
        return Response({'message': '修改成功'}, status=status.HTTP_200_OK)
