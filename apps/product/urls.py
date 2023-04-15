from rest_framework.decorators import action
from django.urls import path
from .views import SearchView, ProductView
from rest_framework import routers

app_name = 'core'
router = routers.DefaultRouter()
# router.register('product', ProductView, basename='product')

router.register('search', SearchView, basename='search')
urlpatterns = [
    path('product/list/',
         ProductView.as_view({'get': 'list'}), name='product-list'),
    path('product/<slug:slug>/',
         ProductView.as_view({'get': 'retrieve'}), name='product-detail'),
]
urlpatterns += router.urls
