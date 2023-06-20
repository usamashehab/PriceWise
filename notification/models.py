from django.db import models

# Create your models here.


class Notification(models.Model):
    user = models.ForeignKey('user.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    favorite = models.ForeignKey('favorite.Favorite', on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
