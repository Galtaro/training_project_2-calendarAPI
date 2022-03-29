from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="email", unique=True)
    country = models.CharField(max_length=25, verbose_name="country", blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "country"]

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'





