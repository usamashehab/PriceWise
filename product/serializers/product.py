from rest_framework import serializers
from ..models import Product, Price


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('price', 'date')


class ProductSerializer(serializers.ModelSerializer):
    price_history = PriceSerializer(read_only=True, many=True)

    class Meta:
        model = Product
        exclude = ('search_vector', )
        depth = 1
