from django.db import models

from accounts.models import CustomUser, Country


class Event(models.Model):
    user = models.ManyToManyField(
        CustomUser,
        related_name="custom_user_event",
        blank=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name="event_name"
    )
    start_datetime = models.DateTimeField(
        verbose_name="event_start_datetime"
    )
    end_datetime = models.DateTimeField(
        blank=True,
        verbose_name="event_end_datetime"
    )

    """
    The value of next attribute is set by default by migration 
    '0002_add_default_value_for_Notification.py'.
    It is necessary to create the first record in the database table    
    """

    notification = models.ForeignKey(
        "Notification",
        on_delete=models.SET_DEFAULT,
        default=1,
        verbose_name="notification_event"
    )

    country_holiday = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="country_event"
    )

    official_holiday = models.BooleanField(default=False, db_index=True)

    def save(self, *args, **kwargs):
        if not self.end_datetime:
            self.end_datetime = self.start_datetime.replace(
                hour=23,
                minute=59,
                second=00
            )
        super().save(*args, **kwargs)

    objects = models.Manager()


class Notification(models.Model):
    description = models.CharField(
        max_length=80,
        verbose_name="notification_description"
    )
    value_time = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name="notification_value_time"
    )

    def __str__(self):
        if self.value_time is None:
            return "---"
        return str(self.description)

    objects = models.Manager()
