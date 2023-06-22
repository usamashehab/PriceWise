from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    subcategory = serializers.SerializerMethodField('get_subcategory')

    class Meta:
        model = Category
        fields = '__all__'

    def get_subcategory(self, obj):
        subcategories = obj.subcategory.all()
        return CategorySerializer(subcategories, many=True).data
