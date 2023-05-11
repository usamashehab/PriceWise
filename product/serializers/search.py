
from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    search = serializers.CharField(write_only=True)
