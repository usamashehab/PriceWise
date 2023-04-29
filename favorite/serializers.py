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

    def create(self, validated_data):
        user = self.context['request'].user
        return Favorite.objects.create(user=user, **validated_data)
