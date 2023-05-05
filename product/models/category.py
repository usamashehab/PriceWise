from django.db import models
from uuid import uuid4
from django.utils.text import slugify


def categor_image_path(instance, filename):
    """generate image's name using uuid

    Arguments:
        filename -- name of the image

    Returns:
        return name in (xxxxxxxx-xxxx-mxxx-nxxx-xxxxxxxxxxxx.ext) format
        exe is extenstion of the image
    """

    ext = filename.split(".")[-1]
    filename = "%s.%s" % (uuid4(), ext)
    return "category/images/{0}".format(filename)


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            null=False, blank=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategory')

    image = models.ImageField(upload_to=categor_image_path)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
