from rest_framework import serializers

from ..models import StockInfo


class StockInfoSerializer(serializers.ModelSerializer):
    """商品供应商序列化器"""

    class Meta:
        model = StockInfo
        fields = '__all__'
