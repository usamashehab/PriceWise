from .fields import (
    MainFields,
    OperatingSystem,
    Connectivity,
    GeneralStorage,
    Storage,
    Display,
    Connectivity,
    Processor,
    Graphics,
    Battery
)
from django.db import models


class Mobile(MainFields, OperatingSystem, Connectivity, GeneralStorage, Display, Battery):

    def __str__(self):
        return f"{self.product.brand} {self.model_name}"


class TV(MainFields, Connectivity, Display):
    smart_tv = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.brand} {self.model_name}"


class Laptop(MainFields, OperatingSystem, Processor, Display, Graphics, Battery, Storage):

    def __str__(self):
        return f"{self.product.brand} {self.model_name}"


class Tablet(MainFields, OperatingSystem, Connectivity, Display, Battery, GeneralStorage):

    def __str__(self):
        return f"{self.product.brand} {self.model_name}"
