# models
from django.db import models
from datetime import date
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex
from product.models.category import Category
from product.models.vendor import Vendor
# utils
from django.utils.text import slugify
# from django.utils.translation import gettext_lazy as _

from datetime import date
from decimal import Decimal

class ProductManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related(
            'vendor',
            'category'
        ).prefetch_related(
            'price_history',
            'images'
        )

    def create_or_update(self, **kwargs):
        uid = kwargs.pop('uid')
        category = Category.objects.get(name=kwargs.pop('category'))
        vendor = Vendor.objects.get(name=kwargs.pop('vendor'))
        #  should pass Category and Vendor as An object
        product, created = Product.objects.get_or_create(uid=uid,
                                                        vendor=vendor, category=category,
                                                        defaults=kwargs)

        if not created:
            new_price = Decimal(kwargs.get('price')) if kwargs.get('price') is not None else None 
            new_sale_price = Decimal(kwargs.get('sale_price')) if kwargs.get('sale_price') is not None else None

            # Product exists, update its price and sale_price fields
            if product.price != new_price or product.sale_price != new_sale_price:
                old_price = product.price
                old_sale_price = product.sale_price
                Product.objects.filter(uid=uid, vendor=vendor).update(price=new_price, sale_price=new_sale_price)
                Price.objects.get_or_create(
                    product=product,
                    price=old_sale_price if old_sale_price is not None else old_price,
                    date=date.today()
                )
        else:
            price = Decimal(kwargs.get('sale_price')) if kwargs.get('sale_price') is not None \
                else Decimal(kwargs.get('price')) if kwargs.get('price') is not None \
                else None
            price_history, created = Price.objects.get_or_create(
                product=product,
                price=price,
                date=date.today()
            )
            if created:
                price_history.save()

        return product, created


class Product(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(null=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    brand = models.CharField(max_length=50, null=True)
    vendor = models.ForeignKey(
        "product.Vendor",
        on_delete=models.CASCADE,
        related_name='products',
    )
    category = models.ForeignKey(
        "product.Category",
        on_delete=models.CASCADE,
        related_name='products',
    )
    available = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    sale_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    uid = models.CharField(max_length=255)
    rating = models.DecimalField(
        max_digits=4, decimal_places=2, default=0.00, null=True, blank=True)
    views = models.PositiveIntegerField(default=0)
    reviews = models.PositiveIntegerField(default=0)
    search_vector = SearchVectorField(null=True, blank=True)

    objects = ProductManager()
    class Meta(object):
        indexes = [GinIndex(fields=['search_vector'])]
        unique_together = ('vendor', 'uid')

    def save(self, *args, **kwargs):
        """
        save twice when create new product because at the first time
        search_vector won't update tell there is a save values for the 
        fields title and description
        """
        self.slug = slugify(self.title) + self.uid

        # if not self.pk:
        #     super().save(*args, **kwargs)
        #     if not self.search_vector:
        #         self.search_vector = SearchVector('title', 'description', 'brand')
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title or "empty title"


class Price(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(default=date.today)

    class Meta:
        ordering = ['-date']


class Image(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.CharField(max_length=50)
    # alt = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)
        unique_together = ('product', 'order')

    def __str__(self):
        return self.alt or "empty alt"
