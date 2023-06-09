from cart.models import Cart
from django.db import transaction
from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from users.models import Address, Users, ClubCard

from common.default_permission import BasePermission
from common.pay import ALiPay
from common.shop_config import VIP_DISCOUNT
from .models import Order, OrderGoods, OrderComment
from .serializers import OrderSerializer, OrderCommentSerializer, OrderGoodsSerializer


class OrderView(GenericViewSet, mixins.ListModelMixin):
    """订单视图"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, BasePermission]
    filterset_fields = ['status']  # 可以实现通过参数查询功能

    @transaction.atomic  # 添加事务
    def create(self, request, *arg, **kwargs):
        address = request.data.get('address')
        if not Address.objects.filter(user=request.user, id=address).exists():
            return Response({'error': '传入的收货地址ID错误'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        address_obj = Address.objects.get(id=address, user=request.user)
        cart_goods = Cart.objects.filter(user=request.user, is_checked=True)
        if not cart_goods.exists():
            return Response({'error': '订单提交失败，未选中商品'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        save_id = transaction.savepoint()  # 创建保存节点
        try:
            order = Order.objects.create(user=request.user, address=address_obj.merge_address, amount=0)
            order.set_order_number()
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
                    return Response({'error': f'{cart.goods.name}库存不足'},
                                    status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                OrderGoods.objects.create(
                    order=order, goods=cart.goods, number=cart.number, price=cart.goods.price)
                cart.delete()
            if ClubCard.objects.filter(user=request.user).exists():
                amount = float(amount) * VIP_DISCOUNT
            order.amount = amount
            order.save()
        except Exception:
            transaction.savepoint_rollback(save_id)
            return Response({'error': '服务器异常，创建订单失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            transaction.savepoint_commit(save_id)
            ser = self.get_serializer(order)
            return Response(ser.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """获取订单详情"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        goods = OrderGoods.objects.filter(order=instance)
        order_goods = OrderGoodsSerializer(goods, many=True)
        result = serializer.data
        result['goods_list'] = order_goods.data
        return Response(result)

    def close_order(self, request, *args, **kwargs):
        """关闭订单"""
        obj = self.get_object()
        if obj.status != 1:
            return Response(
                {'error': '订单状态错误'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY
            )
        obj.status = 6
        obj.save()
        return Response({'message': '订单已关闭'}, status=status.HTTP_200_OK)


class OrderCommentView(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    """订单商品评价视图"""
    queryset = OrderComment.objects.all()
    serializer_class = OrderCommentSerializer
    permission_classes = [IsAuthenticated, BasePermission]
    filterset_fields = ['goods', 'order']

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        order = request.data.get('order')
        if not order:
            return Response({'error': '订单ID错误'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if not Order.objects.filter(id=order).exists():
            return Response({'error': '订单不存在'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        order_obj = Order.objects.get(id=order)
        if order_obj.status != 4:
            return Response({'error': '不存在未评价订单'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        if order_obj.user != request.user:
            return Response({'error': '你不能评价此订单'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        comment = request.data.get('comment')
        if not isinstance(comment, list):
            return Response({'error': '订单评价参数格式有误'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        save_id = transaction.savepoint()
        try:
            for item in comment:
                if not isinstance(item, dict):
                    return Response({'error': '订单评价参数格式有误'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                goods = item.get('goods', None)
                if not OrderGoods.objects.filter(order=order_obj, goods__id=goods).exists():
                    return Response({'error': '订单中没有该商品'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                item['user'] = request.user.id
                item['goods'] = goods
                ser = OrderCommentSerializer(data=item)
                ser.is_valid()
                ser.save()
            order_obj.status = 5
            order_obj.save()
        except Exception:
            transaction.savepoint_rollback(save_id)
            return Response({'error': '评价失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            transaction.savepoint_commit(save_id)
            return Response({'message': '评论成功'}, status=status.HTTP_201_CREATED)


class OrderPayView(GenericViewSet):
    """订单支付接口"""
    permission_classes = [IsAuthenticated]

    def check(self, request):
        order_id = request.data.get('orderID')
        if not Order.objects.filter(id=order_id, user=request.user).exists():
            return Response({'error': '订单不存在'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        order = Order.objects.get(id=order_id)
        amount = order.amount
        if ClubCard.objects.filter(user=request.user).exists():
            card = ClubCard.objects.get(user=request.user)
            if card.money >= amount:
                return Response({'club': 'YES', 'message': '会员余额可支付'}, status=status.HTTP_200_OK)
            else:
                return Response({'club': 'NO', 'message': '会员余额不足'}, status=status.HTTP_200_OK)
        return Response({'club': 'NO', 'message': '非会员'}, status=status.HTTP_200_OK)

    def club_pay(self, request):
        order = Order.objects.get(id=request.data.get('orderID'))
        card = ClubCard.objects.get(user=request.user)
        card.money -= order.amount
        order.status = 4
        card.save()
        order.save()
        return Response({'message', '使用会员余额成功支付'}, status=status.HTTP_200_OK)

    def ali_pay(self, request):
        order = Order.objects.get(id=request.data.get('orderID'))
        amount = order.amount
        order_number = order.order_number
        title = '订单支付'
        pay_url = ALiPay().mobile_payment_url(order_number, amount, title)
        return Response({'pay_url': pay_url}, status=status.HTTP_200_OK)
