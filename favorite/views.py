from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from .models import Favorite
from .serializers import FavoriteSerializer, UpdateFavoriteSerializer
from rest_framework.permissions import IsAuthenticated


class FavoriteView(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin
):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    # permission_classes = (IsAuthenticated,)  # TODO: uncomment this line
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_queryset(self):
        user = self.request.user
        return Favorite.objects.filter(user=user)

    def get_serializer_class(self):
        if self.action == 'partial_update':
            return UpdateFavoriteSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

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
