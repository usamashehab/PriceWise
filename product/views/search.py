from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from ..models import Product
from django.db.models import Count
from ..serializers import ProductSerializer, SearchSerializer
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import F, Q
from utils import get_filter_attrs


class SearchView(viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = SearchSerializer

    @action(methods=['post'], detail=False)
    def search(self, request, search):
        search_query = SearchQuery(search)
        filters = request.data.get('filters', {})
        filters = [Q(**{k: v}) for k, v in filters.items()]
        # filters = list(map(lambda x: Q(**{x: filters[x]}), filters))

        products = Product.objects.annotate(
            similarity=TrigramSimilarity('title', search),
            rank=SearchRank(F('search_vector'), search_query)
        ).filter(
            Q(search_vector=search_query) |
            Q(similarity__gt=0.08) |
            Q(title__icontains=search),
            *filters
        ).order_by(
            '-similarity',
            '-rank'
        )
        category = products.values('category__name').annotate(
            count=Count('category')).order_by('-count').first()
        filter_attrs = {}
        if category:
            category_name = category.get('category__name')
            filter_attrs = get_filter_attrs(category_name, products)
        page = self.paginate_queryset(products)
        payload = {
            "filter": filter_attrs,
        }
        if page is not None:
            # used CompanyProfileSerializer to serialize the companies query
            serializer = ProductSerializer(page, many=True)
            payload['products'] = serializer.data
            return self.get_paginated_response(payload)

        serializer = self.get_serializer(products, many=True)
        payload['products'] = serializer.data
        return Response(payload, status=200)
