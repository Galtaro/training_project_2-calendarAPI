from django.db import IntegrityError
from django.dispatch import receiver
from djoser.signals import user_activated
from rest_framework import status
from rest_framework.response import Response

from events.models import Event, CustomUserEvent


@receiver(user_activated)
def add_official_holidays_to_custom_user(user, **kwargs):
    country = user.country
    if country:
        queryset_event = Event.objects.filter(
            country_holiday=country,
            official_holiday=True
        )
        added_events = []
        for event in queryset_event:
            try:
                CustomUserEvent.objects.create(
                    user=user,
                    event=event
                )
                event_name = event.name
                added_events.append(event_name)
            except IntegrityError:
                continue
        return Response(
            {'added_events': added_events},
            status=status.HTTP_200_OK
        )
