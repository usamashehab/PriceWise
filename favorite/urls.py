from rest_framework.routers import DefaultRouter
from .views import FavoriteView


router = DefaultRouter()
router.register("favorites", FavoriteView, basename='Favorites')

urlpatterns = router.urls
