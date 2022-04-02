from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="email", unique=True)
    country = models.ForeignKey(
        "Country",
        on_delete=models.SET_DEFAULT,
        default=1,
        related_name="country_custom_user")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta(AbstractUser.Meta):
        swappable = 'AUTH_USER_MODEL'


class Country(models.Model):
    country_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        unique=True,
        verbose_name="country")

    objects = models.Manager()


