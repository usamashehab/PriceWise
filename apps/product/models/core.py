from django.db import models
from .fields import (
    MainField,
    OperatingSystem,
    Processor,
    Connectivity,
    Camera,
    Display,
    Battery,
    Graphics,
    StorageRam,
    Hdmi
)


class Mobile(MainField,
             OperatingSystem,
             Processor,
             Connectivity,
             Camera,
             Display,
             Battery,
             Graphics,
             StorageRam):

    def __str__(self):
        return f"{self.product.brand} {self.model}"


class TV(MainField, OperatingSystem, Connectivity, Display, Graphics, Hdmi):
    sound = models.CharField(max_length=50, null=True, blank=True)
    smart_tv = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.product.brand} {self.model}"


class Laptop(MainField, OperatingSystem, Processor, Connectivity, Display, Graphics, Hdmi, Battery, StorageRam):

    def __str__(self):
        return f"{self.product.brand} {self.model}"


class Tablet(MainField, OperatingSystem, Processor, Connectivity, Display, Battery, Graphics, StorageRam):

    def __str__(self):
        return f"{self.product.brand} {self.model}"
