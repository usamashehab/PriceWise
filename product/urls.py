from rest_framework.decorators import action
from django.urls import path
from .views import SearchView, ProductView, CategoryView
from rest_framework import routers

app_name = 'core'
router = routers.DefaultRouter()

router.register('search/', SearchView, basename='search')

urlpatterns = [
    path('product/list/',
         ProductView.as_view({'get': 'list'}), name='product-list'),
    path('product/<slug:slug>/',
         ProductView.as_view({'get': 'retrieve'}), name='product-detail'),
    path('category/<slug:slug>/products/',
         CategoryView.as_view({'get': 'list_products'}), name='category-products'),
    path('category/list/',
         CategoryView.as_view({'get': 'list'}), name='category-list'),
    path('search/<str:search>/',
         SearchView.as_view({'post': 'search'}), name='search'),


]
