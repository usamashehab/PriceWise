from django.urls import path
from .views import SearchView, ProductView, CategoryView
from rest_framework import routers

app_name = 'core'
router = routers.DefaultRouter()

router.register('search', SearchView, basename='search')
router.register('product', ProductView, basename='product')
router.register('category', CategoryView, basename='category')

urlpatterns = router.urls
