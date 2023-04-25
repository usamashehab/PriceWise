from rest_framework import viewsets, mixins
from ..serializers import ProductSerializer
from ..models import Product, Vendor
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import F, Q
from ..serializers import ProductSerializer
from rest_framework.response import Response


class ProductView(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin
                  ):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    http_method_names = ['get']

    def get_object(self):
        slug = self.kwargs.get('slug')
        return self.queryset.filter(slug=slug).first()

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        other_vendors = Vendor.objects.exclude(id=product.vendor.id)
        similar_product_other_vendor = list()
        for vendor in other_vendors:
            search_query = SearchQuery(product.title)
            similar_product = vendor.products.annotate(
                similarity=TrigramSimilarity('title', product.title),
                rank=SearchRank(F('search_vector'), search_query)
            ).filter(Q(search_vector=search_query) | Q(similarity__gt=0.3)).order_by('-similarity', "-rank", "sale_price", "price").first()

            similar_product_other_vendor.append(similar_product)

        similar_products_data = ProductSerializer(
            similar_product_other_vendor,
            many=True
        ).data

        data = {"product": serializer.data,
                "similar_products": similar_products_data}

        return Response(data)
