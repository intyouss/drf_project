import time

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from .models import Order, OrderGoods
from .permissions.order import OrderPermission
from .serializers.order import OrderSerializer
from users.models import Address

from cart.models import Cart


class OrderView(GenericViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrderPermission]

    def create(self, request, *arg, **kwargs):
        address = request.data.get('address')
        if not Address.objects.filter(user=request.user, id=address).exists():
            return Response({'error': '传入的收货地址ID错误'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        address_obj = Address.objects.get(id=address, user=request.user)
        address_str = '{}{}{}{} {} {}'.format(
            address_obj.province,
            address_obj.city,
            address_obj.county,
            address_obj.address,
            address_obj.name,
            address_obj.phone
        )
        cart_goods = Cart.objects.filter(user=request.user, is_checked=True)
        if not cart_goods.exists():
            return Response({'error': '订单提交失败，未选中商品'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        order_number = str(int(time.time())) + str(request.user)
        order = Order.objects.create(user=request.user, address=address_str, order_number=order_number, amount=0)
        amount = 0
        for cart in cart_goods:
            amount += cart.goods.price * cart.number
            OrderGoods.objects.create(
                order=order, goods=cart.goods, number=cart.number, price=cart.goods.price)
        order.amount = amount
        order.save()
        return Response({'message': address_str, 'amount': amount}, status=status.HTTP_201_CREATED)