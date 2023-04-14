from django.urls import path
from .views import SearchView, ProductView
from rest_framework import routers

app_name = 'core'
router = routers.DefaultRouter()
router.register('product', ProductView, basename='product')
router.register('search', SearchView, basename='search')

urlpatterns = router.urls
