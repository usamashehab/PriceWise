from rest_framework import viewsets, mixins
from ..serializers import ProductSerializer
from ..models import Product, Vendor
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import F, Q
from rest_framework.response import Response
from ..signals import product_retrieved
from rest_framework.decorators import action
from django.db.models import F, FloatField


class ProductView(viewsets.GenericViewSet,
                  mixins.RetrieveModelMixin
                  ):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    http_method_names = ['get']
    lookup_field = 'slug'

    def get_object(self):
        slug = self.kwargs.get('slug')
        return self.queryset.filter(slug=slug).first()

    # get the product object
    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        # get all other vendors except current vendor of product
        other_vendors = Vendor.objects.exclude(id=product.vendor.id)

        similar_product_other_vendor = list()
        for vendor in other_vendors:
            # search for similar product of other vendors
            search_query = SearchQuery(product.title)
            similar_product = vendor.products.annotate(
                similarity=TrigramSimilarity('title', product.title),
                rank=SearchRank(F('search_vector'), search_query)
            ).filter(Q(search_vector=search_query) | Q(similarity__gt=0.1)).order_by('-similarity', "-rank", "sale_price", "price").first()
            if similar_product:
                similar_product_other_vendor.append(similar_product)

        similar_products_data = ProductSerializer(
            similar_product_other_vendor,
            many=True
        ).data

        data = {"product": serializer.data,
                "similar_products": similar_products_data}

        # send signal
        product_retrieved.send(sender=Product, instance=product)
        return Response(data)

    @action(methods=['get'], detail=False)
    def deals(self, request):
        products = self.queryset.filter(sale_price__isnull=False).annotate(
            deal=100 - (F('sale_price') / F('price') * 100)
        ).order_by('-deal')
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=200)

    @action(methods=['get'], detail=False, url_path='popular')
    def popular(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
