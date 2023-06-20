from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path


app_name = "user"
router = DefaultRouter()
router.register("users", UserViewSet)

urlpatterns = router.urls
