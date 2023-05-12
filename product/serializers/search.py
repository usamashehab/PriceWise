from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
    search = serializers.CharField(max_length=200)
