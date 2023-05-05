from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from ..models import Product
from ..serializers import SearchSerializer, ProductSerializer


class SearchView(viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = SearchSerializer

    @action(methods=['post'], detail=False, )
    def search(self, request, format=None):
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        page = self.paginate_queryset(serializer.data["products"])
        if page is not None:
            # used CompanyProfileSerializer to serialize the companies query
            serializer = ProductSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
