from .models import Coupon
from rest_framework import serializers
from product.serializers.product import ProductSerializer


class CouponSerializer(serializers.ModelSerializer):
    vendor = serializers.SerializerMethodField('get_vendor', read_only=True)

    def get_vendor(self, obj):
        return obj.vendor.name

    class Meta:
        model = Coupon
        fields = ('id', 'code', 'valid_from', 'valid_to',
                  'discount', 'active', 'product', 'vendor')


class CouponDetailSerializer(CouponSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Coupon
        fields = '__all__'
