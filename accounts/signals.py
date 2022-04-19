from django.dispatch import receiver
from djoser.signals import user_activated

from events.models import Event, CustomUserEvent


@receiver(user_activated)
def add_official_holidays_to_custom_user(sender, user, request, **kwargs):
    country = user.country
    if country:
        queryset_event = Event.objects.filter(
            country_holiday=country,
            official_holiday=True
        )
        for event in queryset_event:
            CustomUserEvent.objects.create(
                user=user,
                event=event
            )

