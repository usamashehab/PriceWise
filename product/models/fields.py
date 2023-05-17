from django.db import models


class MainFields(models.Model):
    model_name = models.CharField(max_length=255, null=True)
    product = models.OneToOneField(
        'product.Product', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class OperatingSystem(models.Model):
    operating_system = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        abstract = True


class Connectivity(models.Model):
    connectivity_tech = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True


class Display(models.Model):
    display_type = models.CharField(max_length=50, null=True, blank=True)
    display_size = models.CharField(max_length=50, null=True, blank=True)
    display_resolution = models.CharField(max_length=50, null=True, blank=True)
    refresh_rate = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        abstract = True

    class Meta:
        abstract = True


class Processor(models.Model):
    cpu_brand = models.CharField(max_length=100, null=True)
    cpu_type = models.CharField(max_length=100, null=True)
    cpu_speed = models.CharField(max_length=50, null=True)
    cpu_num_cores = models.CharField(null=True, max_length=10)

    class Meta:
        abstract = True


class Graphics(models.Model):
    gpu_brand = models.CharField(
        max_length=100, help_text="The type of GPU chip (e.g. NVIDIA, AMD)", null=True)
    gpu_coprocessor = models.CharField(
        max_length=100, help_text="The model of a specific type (e.g AMD Radeon Graphics, ..)", null=True)
    gpu_memory = models.CharField(
        help_text="The amount of memory on the GPU in GB", null=True, max_length=10)

    class Meta:
        abstract = True


class Battery(models.Model):
    battery_capacity = models.CharField(max_length=50, null=True)
    battery_life = models.CharField(max_length=50, null=True)

    class Meta:
        abstract = True


class GeneralStorage(models.Model):
    storage = models.DecimalField(max_digits=7, decimal_places=2 ,null=True)
    ram = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    class Meta:
        abstract = True


class Storage(GeneralStorage):
    storage_type = models.CharField(max_length=50, null=True, default='HDD')
    ram_type = models.CharField(max_length=50, null=True)

    class Meta:
        abstract = True
