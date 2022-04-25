from django.db import models

from accounts.models import CustomUser, Country

STATUS_CHOICES = (
    (False, 'Show only custom events'),
    (True, 'Show only official holidays events'),
)


class Event(models.Model):
    user = models.ManyToManyField(
        CustomUser,
        related_name='custom_user_event',
        through='CustomUserEvent',
        blank=True
    )
    name = models.CharField(
        max_length=100,
        verbose_name='event_name'
    )
    start_datetime = models.DateTimeField(
        verbose_name='event_start_datetime'
    )
    end_datetime = models.DateTimeField(
        blank=True,
        verbose_name='event_end_datetime'
    )

    """
    The value of next attribute is set by default by migration 
    '0002_add_default_value_for_Notification.py'.
    It is necessary to create the first record in the database table    
    """

    notification = models.ForeignKey(
        'Notification',
        on_delete=models.SET_DEFAULT,
        default=1,
        verbose_name='notification_event'
    )

    country_holiday = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='country_event'
    )

    official_holiday = models.BooleanField(
        choices=STATUS_CHOICES,
        default=False,
        db_index=True
    )

    def save(self, *args, **kwargs):
        if not self.end_datetime:
            self.end_datetime = self.start_datetime.replace(
                hour=23,
                minute=59,
                second=00
            )
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'start_datetime', 'end_datetime'],
                name='name_start_datetime_end_datetime_unique'),
        ]

    objects = models.Manager()


class CustomUserEvent(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='custom_user_user_event'
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='event_user_even'
    )
    subscription_status = models.BooleanField(
        default=False,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'event'],
                name='user_event_unique'),
        ]

    objects = models.Manager()


class Notification(models.Model):
    description = models.CharField(
        max_length=80,
        verbose_name='notification_description'
    )
    value_time = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name='notification_value_time'
    )

    def __str__(self):
        if self.value_time is None:
            return '---'
        return str(self.description)

    objects = models.Manager()
