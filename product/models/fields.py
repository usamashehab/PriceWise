from django.db import models


class MainFields(models.Model):
    model = models.CharField(max_length=255)
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)

    class Meta:
        abstract = True


class OperatingSystem(models.Model):
    operating_system = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True


class Connectivity(models.Model):
    wifi = models.CharField(max_length=50, null=True, blank=True)
    bluetooth = models.CharField(max_length=50, null=True, blank=True)
    usb = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        abstract = True


class Hdmi(models.Model):
    hdmi = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Camera(models.Model):
    primary_camera_resolution = models.CharField(
        max_length=50, null=True, blank=True)
    front_camera_resolution = models.CharField(
        max_length=50, null=True, blank=True)

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
    cpu_series = models.CharField(max_length=100)
    # cpu_base_clock_speed = models.DecimalField(
    #     max_digits=5, decimal_places=2)
    # cpu_boost_clock_speed = models.DecimalField(
    #     max_digits=5, decimal_places=2)
    cpu_num_cores = models.PositiveSmallIntegerField()
    cpu_num_threads = models.PositiveSmallIntegerField()
    # cpu_socket_type = models.CharField(max_length=100)
    # cpu_tdp = models.PositiveSmallIntegerField(
    #     help_text="Thermal Design Power (TDP) in watts")
    cpu_cache_memory = models.CharField(max_length=100)

    class Meta:
        abstract = True


class Graphics(models.Model):
    gpu_brand = models.CharField(max_length=100)
    gpu_model = models.CharField(max_length=100)
    # gpu_chip = models.CharField(
    #     max_length=100, help_text="The type of GPU chip (e.g. NVIDIA, AMD)")
    gpu_memory = models.PositiveSmallIntegerField(
        help_text="The amount of memory on the GPU in GB")
    # gpu_memory_type = models.CharField(
    #     max_length=50, help_text="The type of memory used by the GPU (e.g. GDDR5, GDDR6)")
    # gpu_memory_bandwidth = models.CharField(
    #     max_length=50, help_text="The bandwidth of the GPU memory")
    # gpu_clock_speed = models.CharField(
    #     max_length=50, help_text="The clock speed of the GPU in MHz")
    gpu_cuda_cores = models.PositiveSmallIntegerField(
        null=True, blank=True, help_text="The number of CUDA cores on the GPU (for NVIDIA GPUs)")
    # gpu_stream_processors = models.PositiveSmallIntegerField(
    #     null=True, blank=True, help_text="The number of stream processors on the GPU (for AMD GPUs)")
    # gpu_tdp = models.PositiveSmallIntegerField(
    #     help_text="The thermal design power of the GPU in watts")

    class Meta:
        abstract = True


class Battery(models.Model):
    battery_capacity = models.CharField(max_length=50)
    battery_life = models.CharField(max_length=50)

    class Meta:
        abstract = True


class StorageRam(models.Model):
    storage = models.PositiveSmallIntegerField()
    storage_type = models.CharField(max_length=50)
    ram = models.PositiveSmallIntegerField()
    ram_type = models.CharField(max_length=50)

    class Meta:
        abstract = True
