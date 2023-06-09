from rest_framework import status, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, GenericViewSet, ModelViewSet

from common.default_permission import BasePermission, AdminPermission
from .models import GoodsGroup, GoodsCarousel, Goods, Collect, Detail, Supplier, StockInfo
from .serializers import (
    CollectSerializer,
    DetailSerializer,
    GoodsSerializer,
    GoodsCarouselSerializer,
    GoodsGroupSerializer,
    StockInfoSerializer,
    SupplierSerializer
)


class IndexView(APIView):
    """商城首页数据获取的接口"""

    def get(self, request):
        group = GoodsGroup.objects.filter(is_status=True)
        groupSer = GoodsGroupSerializer(group, many=True, context={'request': request})
        carousel = GoodsCarousel.objects.filter(is_status=True)
        carouselSer = GoodsCarouselSerializer(carousel, many=True, context={'request': request})
        goods = Goods.objects.filter(is_recommend=True)
        goodsSer = GoodsSerializer(goods, many=True, context={'request': request})
        result = {
            'group': groupSer.data,
            'carousel': carouselSer.data,
            'goods': goodsSer.data
        }
        return Response(result, status=status.HTTP_200_OK)


class GoodsView(ReadOnlyModelViewSet):
    """商品视图"""
    queryset = Goods.objects.filter(is_on=True)
    serializer_class = GoodsSerializer
    filterset_fields = ('group', 'is_recommend')
    # 通过价格、销量排序、创建时间排序
    ordering_fields = ('sales', 'price', 'created_time')

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        detail = Detail.objects.get(goods=instance)
        result = serializer.data
        result['detail'] = DetailSerializer(detail).data
        return Response(result, status=status.HTTP_200_OK)


class CollectView(
    mixins.DestroyModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    """收藏商品视图"""
    queryset = Collect.objects.all()
    serializer_class = CollectSerializer
    # 设置认证用户才能有权访问
    permission_classes = [IsAuthenticated, BasePermission]

    def create(self, request, *args, **kwargs):
        user = request.user
        params_user_id = request.data.get('user')
        if user.id == params_user_id:
            return super().create(request, *args, **kwargs)
        return Response({'error': '您没有权限执行此操作'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)
        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class GoodsGroupView(mixins.ListModelMixin, GenericViewSet):
    """商品分类视图"""
    queryset = GoodsGroup.objects.filter(is_status=True)
    serializer_class = GoodsGroupSerializer


class GoodsSupplierView(ModelViewSet):
    """商品供应商视图"""
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated, AdminPermission]


class GoodsStockView(
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    """商品入库视图：增删查"""
    queryset = StockInfo.objects.all()
    serializer_class = StockInfoSerializer
    permission_classes = [IsAuthenticated, AdminPermission]
    filterset_fields = ['goods', 'admin', 'producer']

    def create(self, request, *args, **kwargs):
        # 创建入库商品账单，并添加至库存
        stock = StockInfo.objects.create(goods=Goods.objects.get(id=request.data.get('goods')), admin=request.user
                                         , producer=Supplier.objects.get(id=request.data.get('producer'))
                                         , price=request.data.get('price')
                                         , number=request.data.get('number'))
        stock.goods.stock += stock.number
        stock.goods.save()
        return Response({'message': '添加成功'}, status=status.HTTP_201_CREATED)