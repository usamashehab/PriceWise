from rest_framework import serializers
from .models import Notification
from favorite.serializers import FavoriteSerializer


class NotificationSerializer(serializers.ModelSerializer):

    favorite = FavoriteSerializer(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'title',
            'favorite',
        ]
