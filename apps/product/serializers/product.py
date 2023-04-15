from rest_framework import serializers
from ..models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'slug',
            'url',
            'description',
            'brand',
            'vendor',
            'category',
            'available',
            'price',
            'sale_price',

        ]

        depth = 1
