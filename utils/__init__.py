from django.core.cache import cache
from django.db.models import Count
from product.models import (
    Mobile,
    Laptop,
    TV,
    Tablet,
    Category
)
from .debug import query_debugger

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


def get_filter_attrs(category_name, products, search=None):
    model_lower_name = category_name.lower()
    attrs_dict = {}
    if not attrs_dict:
        for key in filter_attrs[category_name]:
            query_params = {f"{key}__isnull": False}
            attrs = model[category_name].objects.filter(**query_params, product__in=products).values(
                key).annotate(count=Count(key)).order_by(key).values_list(key, 'count')

            print(attrs)
            if attrs:
                attrs_dict[f"{model_lower_name}__{key}"] = attrs

        attrs_dict['category'] = get_categories()
        attrs_dict['brand'] = get_brands(products)
    return attrs_dict


def get_categories():
    categories = Category.objects.all().values_list('id', 'name')
    return categories


def get_brands(products):

    brands = {product.brand for product in products if product.brand is not None}
    return brands
