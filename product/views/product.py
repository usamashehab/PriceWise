from rest_framework import viewsets, mixins
from ..serializers import ProductSerializer, DealSerializer
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

    def get_serializer_class(self):
        if self.action == 'deals':
            return DealSerializer
        return super().get_serializer_class()
    # get the product object

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        if product:
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

            same_products_data = ProductSerializer(
                similar_product_other_vendor,
                many=True
            ).data

            category = product.category
            parent_category = category.parent
            if parent_category:
                similar_products = Product.objects.filter(
                    category__parent=parent_category)[:15]
            else:
                similar_products = Product.objects.filter(
                    category=category)[:15]

            similar_products = ProductSerializer(
                similar_products, many=True).data

            data = {"product": serializer.data,
                    "same_product_other_vendor": same_products_data,
                    "similar_products": similar_products}

            # send signal to increase view count
            product_retrieved.send(sender=Product, instance=product)
            return Response(data)

        return Response({'message': 'Product not found'}, status=404)

    @action(methods=['get'], detail=False, url_path='(?P<category_slug>[^/]+)/deals')
    def deals(self, request, *args, **kwargs):
        category_slug = kwargs.get('category_slug')
        if category_slug == 'all':
            category_slug = None
        if category_slug:
            self.queryset = self.queryset.filter(category__slug=category_slug)

        products = self.queryset.filter(sale_price__isnull=False).annotate(
            deal=100 - (F('sale_price') / F('price') * 100)
        ).order_by('-deal')
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True)
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
