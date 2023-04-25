# models
from django.db import models
from datetime import date
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex
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


class Product(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField()
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    brand = models.CharField(max_length=50)
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

    class Meta(object):
        indexes = [GinIndex(fields=['search_vector'])]
        unique_together = ('vendor', 'uid')

    def save(self, *args, **kwargs):
        """
        save twice when create new product because at the first time
        search_vector won't update tell there is a save values for the 
        fields title and description
        """
        self.slug = slugify(self.title)

        if self.pk:
            super().save(*args, **kwargs)
            self.search_vector = SearchVector(
                'title', 'description', 'brand', 'category__name')
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
    image_url = models.URLField()
    alt = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)
        unique_together = ('product', 'order')

    def __str__(self):
        return self.alt or "empty alt"
