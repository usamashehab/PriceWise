from django.db import models


class Vendor(models.Model):

    class VendorNames(models.TextChoices):
        AMAZON = 'Amazon', 'Amazon'
        JUMIA = 'Jumia', 'Jumia'
        NOON = 'Noon', 'Noon'

    name = models.CharField(
        max_length=255, choices=VendorNames.choices, null=False, blank=False)

    def __str__(self) -> str:
        return self.name or 'empty name'
