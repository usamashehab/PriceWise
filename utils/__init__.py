from django.core.cache import cache
from django.db.models import Count
from product.models import (
    Mobile,
    Laptop,
    TV,
    Tablet,
    Category
)


common_attrs = [
    "ram",
    "storage",
    "display_size",
    "display_type",
    "operating_system",
]
filter_attrs = {
    "Mobile": common_attrs,
    "Laptop": common_attrs,
    "TV": [
        "display_size",
        "display_type",
        "refresh_rate",
        "smart_tv"


    ],
    "Tablet": common_attrs,
    "General": [
        "name",

    ]
}


model = {
    "Mobile": Mobile,
    "Laptop": Laptop,
    "TV": TV,
    "Tablet": Tablet,
}


def get_filter_attrs(category_name, products):
    cache_key = f"filtered_attrs_{category_name}"
    attrs = cache.get(cache_key)
    if attrs is not None:
        return attrs
    model_lower_name = category_name.lower()
    # If the result is not in the cache, do the query and cache the result
    attrs_dict = {
        f"{model_lower_name}__{key}": model[category_name].objects.filter(**{f"{key}__isnull": False}).values(key).annotate(
            count=Count(key)).order_by(key).values_list(key, 'count')
        for key in filter_attrs[category_name]
    }
    attrs_dict['category'] = get_categories()
    attrs_dict['brand'] = get_brands(products)
    cache.set(cache_key, attrs_dict, timeout=60*60*24)
    return attrs_dict


def get_categories():
    cache_key = f"categories"
    categories = cache.get(cache_key)
    if categories is not None:
        return categories

    # If the result is not in the cache, do the query and cache the result
    categories = Category.objects.all().values_list('id', 'name')
    cache.set(cache_key, categories, timeout=60*60*24)
    return categories


def get_brands(products):
    cache_key = f"brands"
    brands = cache.get(cache_key)
    if brands is not None:
        return brands
    brands = products.values('brand').annotate(count=Count(
        'brand')).order_by('brand').values_list('brand', 'count')

    cache.set(cache_key, brands, timeout=60*60*24)
    return brands
