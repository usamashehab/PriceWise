from rest_framework import serializers


class SearchSerializer(serializers.Serializer):
<<<<<<< HEAD
    search = serializers.CharField(write_only=True)
    products = ProductSerializer(many=True, read_only=True)

    def validate(self, attrs):
        search = attrs.pop('search', None)
        search_query = SearchQuery(search)
        # products = Product.objects.annotate(
        #     similarity=TrigramSimilarity('title', search),
        #     rank=SearchRank(F('search_vector'), search_query)
        # ).filter(Q(search_vector=search_query) | Q(similarity__gt=0.1)).order_by('-similarity', "-rank")
        products = Product.objects.annotate(
            similarity=TrigramSimilarity('title', search),
            rank=SearchRank(F('search_vector'), search_query)
        ).filter(Q(search_vector=search_query) | Q(similarity__gt=0.1) | Q(title__icontains=search)).order_by('-similarity', "-rank")

        attrs['products'] = products
        return attrs
=======
    search = serializers.CharField(max_length=200)
>>>>>>> 96235974e117b8bde20980e17a074e52bca58b86
