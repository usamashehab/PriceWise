from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .validators import validate_password_strength
from .managers import CustomUserManager
from favorite.models import Favorite


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    favourties = models.ManyToManyField(
        'product.Product', through=Favorite, related_name='users')

    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def set_password(self, password):
        validate_password_strength(password)
        return super().set_password(password)
