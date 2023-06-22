from rest_framework.routers import DefaultRouter
from .views import CouponView

router = DefaultRouter()
router.register('coupon', CouponView, basename='coupon')

urlpatterns = router.urls
