from django.db import models
from django.utils.timezone import now
# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    favorite = models.ForeignKey('favorite.Favorite', on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
