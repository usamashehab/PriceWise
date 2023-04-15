from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True,
                            null=False, blank=False)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategory')

    def __str__(self) -> str:
        return self.name
