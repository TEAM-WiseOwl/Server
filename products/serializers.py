from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'product_price', 'product_img']


class ProductCartSerializer(serializers.ModelSerializer):
    product_cnt = serializers.IntegerField(default=1)  # 기본 수량은 1로 설정

    class Meta:
        model = Product
        fields = ['product_id', 'product_name', 'product_price', 'product_cnt', 'product_img']