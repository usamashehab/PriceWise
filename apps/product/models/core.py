from django.db import models
from .fields import *


class Mobile(MainFields,
             OperatingSystem,
             ConnectivityTech,
             GeneralStorage):
    screen_size = models.DecimalField(max_digits=3, decimal_places=1)

    def __str__(self):
        return f"{self.product.brand} {self.model}"


class TV(MainFields, ConnectivityTech, Display):
    smart_tv = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.brand} {self.model}"


class Laptop(MainFields, OperatingSystem, Processor, Display, Graphics, Battery, Storage):

    def __str__(self):
        return f"{self.product.brand} {self.model}"

