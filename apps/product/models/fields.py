from django.db import models


class MainFields(models.Model):
    model = models.CharField(max_length=255)
    brand = models.CharField(max_length=50)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class OperatingSystem(models.Model):
    operating_system = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True

class ConnectivityTech(models.Model):
    connectivity_tech = models.CharField(max_length=50, null=True, blank=True)
    class Meta:
        abstract = True


class Display(models.Model):
    display_type = models.CharField(max_length=50, null=True, blank=True)
    display_size = models.CharField(max_length=50, null=True, blank=True)
    display_resolution = models.CharField(max_length=50, null=True, blank=True)
    refresh_rate = models.IntegerField(null=True, blank=True)

    class Meta:
        abstract = True

    class Meta:
        abstract = True


class Processor(models.Model):
    cpu_brand = models.CharField(max_length=100)
    cpu_type = models.CharField(max_length=100)
    cpu_speed = models.DecimalField(
        max_digits=5, decimal_places=2)
    cpu_num_cores = models.PositiveSmallIntegerField()
    cpu_cache_memory = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Graphics(models.Model):
    gpu_brand = models.CharField(
        max_length=100, help_text="The type of GPU chip (e.g. NVIDIA, AMD)")
    gpu_coprocessor = models.CharField(
        max_length=100, help_text="The model of a specific type (e.g AMD Radeon Graphics, ..)")
    gpu_memory = models.PositiveSmallIntegerField(help_text="The amount of memory on the GPU in GB")
    

    class Meta:
        abstract = True


class Battery(models.Model):
    battery_capacity = models.CharField(max_length=50)
    battery_life = models.CharField(max_length=50)

    class Meta:
        abstract = True

class GeneralStorage(models.Model):
    storage = models.PositiveSmallIntegerField()
    ram = models.PositiveSmallIntegerField()
    class Meta:
        abstract = True

class Storage(GeneralStorage):
    storage_type = models.CharField(max_length=50)
    ram_type = models.CharField(max_length=50)

    class Meta:
        abstract = True

