from rest_framework import serializers
from product.serializers import ProductSerializer
from .models import Favourite


class FavouriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Favourite
        fields = [
            'product',
            'desired_price'
        ]
