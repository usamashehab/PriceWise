from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from ..models import Product
from django.db.models import Count
from ..serializers import SearchSerializer, ProductSerializer
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import F, Q


filter_attrs = {
    "Mobiles": [
        "brand" ,
        "ram" ,
        "storage" ,
        "camera" ,
    ]
       , 
}

class SearchView(viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = SearchSerializer

    @action(methods=['post'], detail=False, )
    def search(self, request, format=None):
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        search = serializer.validated_data["search"]
        search_query = SearchQuery(search)
        products = Product.objects.annotate(
            similarity=TrigramSimilarity('title', search),
            rank=SearchRank(F('search_vector'), search_query)
        ).filter(Q(search_vector=search_query) | Q(similarity__gt=0) | Q(title__icontains=search)).order_by('-similarity', "-rank")
        category = products.values('category__name').annotate(
            count=Count('category')).order_by('-count').first()
        print(category)
        page = self.paginate_queryset(products)

        if page is not None:
            # used CompanyProfileSerializer to serialize the companies query
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
