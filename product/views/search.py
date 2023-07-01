from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from ..models import Product
from django.db.models import Count
from ..serializers import ProductSerializer, SearchSerializer
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import F, Q
from utils import get_filter_attrs
from django.db.models import Min, Max
from django.core.cache import cache
from utils import query_debugger


class SearchView(viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = SearchSerializer

    @action(methods=['post'], detail=False, url_path='products/(?P<search>[^/]+)')
    def search(self, request, search):
        search_query = SearchQuery(search)
        filters = request.data.get('filters', {})
        min_price, max_price = request.data.get('price', (0, 1000000))
        filters = [Q(**{f'{k}__in': v}) for k, v in filters.items()]
        # filters = list(map(lambda x: Q(**{x: filters[x]}), filters))

        sort = request.data.get('sort_by', None)
        sort_keyword = self.get_sort_keyword(sort)
        cache_key = f'search_{search}_products'
        products = cache.get(cache_key)
        if not products:
            products = Product.objects.annotate(
                similarity=TrigramSimilarity('title', search),
                rank=SearchRank(F('search_vector'), search_query)
            ).filter(
                Q(search_vector=search_query) |
                Q(similarity__gt=0.1) |
                Q(title__icontains=search),
                Q(price__range=(min_price, max_price)),
                *filters
            ).order_by(
                *sort_keyword
            )

        cache.set(cache_key, products, 60*3)

        category = products.values('category__name').annotate(
            count=Count('category')).order_by('-count').first()
        filter_attrs = {}
        if category:
            category_name = category.get('category__name')
            filter_attrs = get_filter_attrs(
                category_name, products, search)
        page = self.paginate_queryset(products)

        prices = products.aggregate(
            min_price=Min('price'), max_price=Max('price'))
        payload = {
            "filter": filter_attrs,
            "prices": prices
        }

        if page is not None:
            # used CompanyProfileSerializer to serialize the companies query

            serializer = ProductSerializer(page, many=True)
            payload['products'] = serializer.data
            print(type(payload["products"]))
            return self.get_paginated_response(payload)

        serializer = self.get_serializer(products, many=True)
        payload['products'] = serializer.data

        return Response(payload, status=200)

    def get_sort_keyword(self, keyword):
        keywords = {
            'price_low_to_high': 'price',
            'price_high_to_low': '-price',
            'sale_low_to_high': 'deal',
            'sale_high_to_low': '-deal',
        }
        args = ['-similarity',
                '-rank',
                ]
        if keyword and keyword in keywords:
            args = [keywords.get(keyword)] + args

        return args
