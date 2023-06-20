from rest_framework.response import Response
from rest_framework import viewsets, mixins
from .models import Notification
from rest_framework.permissions import IsAuthenticated
from .serializers import NotificationSerializer
from .signals import notification_retrieved


class NotificatinView(viewsets.GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.RetrieveModelMixin):

    permission_classes = [IsAuthenticated]
    serializer_class = NotificationSerializer

    def get_queryset(self):
        user = self.request.user
        return Notification.objects.filter(user=user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        notification_retrieved.send(sender=Notification, instance=instance)
        return Response(serializer.data)
