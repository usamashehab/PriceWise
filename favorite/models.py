from django.db import models


class Favorite(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    desired_price = models.DecimalField(max_digits=10, decimal_places=2)
    desired_price_reached = models.BooleanField(default=False)
