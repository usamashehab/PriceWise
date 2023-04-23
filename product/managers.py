from datetime import date
from decimal import Decimal
from django.db import models
from .models import Product, Price


class ProductManager(models.Manager):

    def create_or_update(self, **kwargs):
        uid = kwargs.pop('uid')
        vendor = kwargs.pop('vendor')

        product, created = Product.objects.get_or_create(
            uid=uid, vendor=vendor, defaults=kwargs)

        if not created:
            new_price = Decimal(kwargs.get('price'))
            new_sale_price = kwargs.get('sale_price')

            if new_sale_price:
                new_sale_price = Decimal(new_sale_price)

            # Product exists, update its price and sale_price fields
            if product.price != new_price or product.sale_price != new_sale_price:
                old_price = product.price
                product.price = new_price
                product.sale_price = new_sale_price
                product.save()
                Price.objects.create(
                    product=product,
                    price=old_price,
                    date=date.today()
                )

        return product
