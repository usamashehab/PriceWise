from rest_framework import serializers
from ..models import (
    Product,
    Price,
    Mobile,
    TV,
    Laptop,
    Tablet
)


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('price', 'date')


class MobileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mobile
        fields = [
            'id',
            'model_name',

        ]


class ProductSerializer(serializers.ModelSerializer):
    price_history = PriceSerializer(read_only=True, many=True)
    mobile = MobileSerializer(read_only=True)

    class Meta:
        model = Product
        exclude = ('search_vector',)
        depth = 1


class TVSerializer(serializers.ModelSerializer):

    class Meta:
        model = TV
        fields = '__all__'


class LaptopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Laptop
        fields = '__all__'


class TabletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tablet
        fields = '__all__'
