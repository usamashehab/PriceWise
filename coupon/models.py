from django.db import models
from django.utils.timezone import now
from product.models import Product
# Create your models here.


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount = models.FloatField()
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    active = models.BooleanField(default=True)
    created = models.DateTimeField(default=now)
    product = models.ForeignKey(
        'product.Product', null=True, blank=True, on_delete=models.CASCADE, related_name='coupons')
    vendor = models.ForeignKey('product.Vendor', on_delete=models.CASCADE)
    url = models.URLField(max_length=200, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.url:
                self.product = Product.objects.filter(url=self.url).first()
        super().save(*args, **kwargs)
