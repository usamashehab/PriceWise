from rest_framework import serializers
from product.serializers import ProductSerializer
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = [
            'product',
            'desired_price'
        ]
