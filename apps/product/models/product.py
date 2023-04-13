# models
from django.db import models

from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex
# utils
from django.utils.translation import gettext_lazy as _


class Product(models.Model):
    # (universal product code)
    upc = models.CharField(max_length=20)
    title = models.CharField(max_length=255)
    url = models.URLField()
    image_url = models.URLField()
    description = models.TextField()
    Brand = models.CharField(_(""), max_length=50)
    vendor = models.ForeignKey("product.Vendor", on_delete=models.CASCADE)
    category = models.ForeignKey("product.Category", on_delete=models.CASCADE)
    available = models.BooleanField(default=True)
    current_price = models.DecimalField(max_digits=8, decimal_places=2)

    search_vector = SearchVectorField(null=True, blank=True)

    class Meta(object):
        indexes = [GinIndex(fields=['search_vector'])]

    def save(self, *args, **kwargs):
        """
        save twice when create new product because at the first time
        search_vector won't update tell there is a save values for the 
        fields title and description
        """

        if self.pk:
            super().save(*args, **kwargs)
            self.search_vector = SearchVector(
                'title', 'description')
        super().save(*args, **kwargs)


class Price(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='price_history')
    price = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-date']



