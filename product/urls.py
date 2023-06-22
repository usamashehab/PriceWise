from django.urls import path
from .views import SearchView, ProductView, CategoryView
from rest_framework import routers

app_name = 'core'
router = routers.DefaultRouter()

router.register('search', SearchView, basename='search')
router.register('product', ProductView, basename='product')
router.register('category', CategoryView, basename='category')

urlpatterns = [

    path('category/<slug:slug>/products/',
         CategoryView.as_view({'get': 'list_products'}), name='list_products'),
]
urlpatterns += router.urls
