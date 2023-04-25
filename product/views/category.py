from rest_framework import viewsets, mixins
from ..serializers import ProductSerializer, CategorySerializer

from ..models import Category
from rest_framework.response import Response


class CategoryView(viewsets.GenericViewSet,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin
                   ):
    serializer_class = ProductSerializer
    queryset = Category.objects.prefetch_related('products').all()
    http_method_names = ['get']

    def get_serializer_class(self):
        if self.action == 'list':
            return CategorySerializer
        return super().get_serializer_class()

    def get_object(self):
        slug = self.kwargs.get('slug')
        return self.queryset.filter(slug=slug).first()

    def retrieve(self, request, *args, **kwargs):
        category = self.get_object()
        serializer = self.get_serializer(category.products, many=True)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
