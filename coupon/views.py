from rest_framework import viewsets, mixins
from .models import Coupon
from .serializers import CouponSerializer, CouponDetailSerializer
from django.utils import timezone


class CouponView(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.RetrieveModelMixin
                 ):
    queryset = Coupon.objects.filter(
        active=True,
        valid_to__gte=timezone.now()
    ).select_related('product', 'vendor')

    http_method_names = ['get']
    serializer_class = CouponSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CouponDetailSerializer
        return super().get_serializer_class()
