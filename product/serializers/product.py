from rest_framework import serializers
from ..models import (
    Product,
    Price,
    Mobile,
    TV,
    Laptop,
    Tablet,
    Image
)


class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields = ('price', 'date')


class MobileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mobile
        exclude = ('product',)


class TVSerializer(serializers.ModelSerializer):

    class Meta:
        model = TV
        exclude = ('product',)


class LaptopSerializer(serializers.ModelSerializer):

    class Meta:
        model = Laptop
        exclude = ('product',)


class TabletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tablet
        exclude = ('product',)


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ('image_url', 'order')


class ProductSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    price_history = PriceSerializer(read_only=True, many=True)
    mobile = MobileSerializer(read_only=True)
    tv = TVSerializer(read_only=True)
    laptop = LaptopSerializer(read_only=True)
    tablet = TabletSerializer(read_only=True)
    deal = serializers.CharField(read_only=True)
    vendor = serializers.SerializerMethodField(
        'get_vendor_name', read_only=True)
    images = ImageSerializer(read_only=True, many=True)
    category = serializers.SerializerMethodField(
        'get_category_name', read_only=True)

    class Meta:
        model = Product
        exclude = ('search_vector',)

    def get_vendor_name(self, obj):
        return obj.vendor.name

    def get_category_name(self, obj):
        return obj.category.name


class DealSerializer(serializers.Serializer):
    category = serializers.IntegerField(required=False)
