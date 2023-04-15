# models
from django.db import models
from datetime import date
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex
# utils
from django.utils.text import slugify
# from django.utils.translation import gettext_lazy as _


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
                'title', 'description')
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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.URLField()
    alt = models.CharField(max_length=255, null=True, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order',)
        unique_together = ('product', 'order')

    def __str__(self):
        return self.alt or "empty alt"
