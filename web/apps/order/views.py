import time

from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.db import transaction
from .models import Order, OrderGoods
from .permissions.order import OrderPermission
from .serializers.order import OrderSerializer
from users.models import Address

from cart.models import Cart


class OrderView(GenericViewSet, mixins.ListModelMixin):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, OrderPermission]
    filterset_fields = ['status']  # 可以实现通过参数查询功能

    @transaction.atomic  # 添加事务
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
        save_id = transaction.savepoint()  # 创建保存节点
        try:
            order = Order.objects.create(user=request.user, address=address_str, order_number=order_number, amount=0)
            amount = 0
            for cart in cart_goods:
                number = cart.number
                amount += cart.goods.price * number
                if cart.goods.stock >= number:
                    cart.goods.stock -= number
                    cart.goods.sales += number
                    cart.goods.save()
                else:
                    transaction.savepoint_rollback(save_id)
                    return Response({'error': f'{cart.goods.name}库存不足'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                OrderGoods.objects.create(
                    order=order, goods=cart.goods, number=cart.number, price=cart.goods.price)
                cart.delete()
            order.amount = amount
            order.save()
        except Exception:
            transaction.savepoint_rollback(save_id)
            return Response({'error': '服务端异常，订单创建失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            transaction.savepoint_commit(save_id)
            ser = self.get_serializer(order)
        return Response(ser.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
