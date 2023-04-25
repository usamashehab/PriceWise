from rest_framework.routers import DefaultRouter
from .views import FavouriteView


router = DefaultRouter()
router.register("favourites", FavouriteView, basename='Favourites')

urlpatterns = router.urls
