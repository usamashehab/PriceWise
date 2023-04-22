from rest_framework.routers import DefaultRouter
from .views import UserViewSet
from django.urls import path
router = DefaultRouter()
router.register("users", UserViewSet)

app_name = "user"
urlpatterns = router.urls

urlpatterns += [
    path('users/activation/<uid>/<token>/',
         UserViewSet.as_view({'post': 'activation'}), name='activation'),
]
