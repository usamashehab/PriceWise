from rest_framework.routers import DefaultRouter
from .views import NotificatinView


app_name = 'notification'

router = DefaultRouter()
router.register('notifications', NotificatinView, basename='notifications')
urlpatterns = router.urls
