from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import GoodsGroup, GoodsCarousel, Goods
from .serializers.goods import GoodsSerializer
from .serializers.goods_carousel import GoodsCarouselSerializer
from .serializers.goods_group import GoodsGroupSerializer


class IndexView(APIView):
    """商城首页数据获取的接口"""

    def get(self, request):
        group = GoodsGroup.objects.filter(is_status=True)
        groupSer = GoodsGroupSerializer(group, many=True)
        carousel = GoodsCarousel.objects.filter(is_status=True)
        carouselSer = GoodsCarouselSerializer(carousel, many=True)
        goods = Goods.objects.filter(is_recommend=True)
        goodsSer = GoodsSerializer(goods, many=True)
        result = {
            'group': groupSer.data,
            'carousel': carouselSer.data,
            'goods': goodsSer.data
        }
        return Response(result, status=status.HTTP_200_OK)