from rest_framework import viewsets, mixins
from ..serializers import ProductSerializer, CategorySerializer

from ..models import Category
from rest_framework.response import Response
from rest_framework.decorators import action


class CategoryView(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   ):
    serializer_class = ProductSerializer
    queryset = Category.objects.prefetch_related('products').all()
    http_method_names = ['get']
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        return super().get_serializer_class()

    def get_object(self):
        slug = self.kwargs.get('slug')
        return self.queryset.filter(slug=slug).first()

    @action(methods=['get'], detail=True, url_path='category/<slug:slug>/products')
    def list_products(self, request, *args, **kwargs):
        category = self.get_object()
        products = category.products.filter(category=category)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(category.products, many=True)
        return Response(serializer.data)
