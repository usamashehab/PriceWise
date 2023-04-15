
from rest_framework import serializers
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from ..models import Product
from django.db.models import F, Q


class SearchSerializer(serializers.Serializer):
    search = serializers.CharField()

    def validate(self, attrs):
        search = attrs.pop('search', None)
        search_query = SearchQuery(search)
        products = Product.objects.annotate(
            similarity=TrigramSimilarity('title', search),
            rank=SearchRank(F('search_vector'), search_query)
        ).filter(Q(search_vector=search_query) | Q(similarity__gt=0.3)).order_by('-similarity', "-rank")

        attrs['products'] = products
        return attrs
