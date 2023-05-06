from rest_framework import serializers
from product.serializers import ProductSerializer
from .models import Favorite
from product.models import Product


class FavoriteSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Favorite
        fields = [
            'product',
            'desired_price'
            'product_id'
        ]

    def create(self, validated_data):
        product = validated_data.pop('product_id', None)
        product = Product.objects.get(id=product)
        user = self.context['request'].user
        return Favorite.objects.create(user=user, product=product ** validated_data)
