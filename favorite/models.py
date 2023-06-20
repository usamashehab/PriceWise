from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    desired_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    price_change_notified = models.BooleanField(default=False)
    notify_when_any_drop = models.BooleanField(default=False)
    last_notified_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        unique_together = ('user', 'product')

    def save(self, *args, **kwargs):
        if not self.pk and self.notify_when_any_drop:
            self.last_notified_price = self.product.price
        super().save(*args, **kwargs)
