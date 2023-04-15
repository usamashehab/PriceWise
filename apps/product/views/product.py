from rest_framework import viewsets, mixins
from ..serializers import ProductSerializer
from ..models import Product


class ProductView(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin
                  ):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    http_method_names = ['get']
