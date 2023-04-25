from rest_framework import viewsets, mixins
from rest_framework.response import Response
from .models import Favourite
from .serializers import FavouriteSerializer


class FavouriteView(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
):
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count = queryset.filter(desired_price_reached=True).count()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        data = {
            'products': serializer.data,
            'count': count
        }
        return Response(data)
