from zoneinfo import ZoneInfo

import requests
from django.core.management.base import BaseCommand
from ics import Calendar
from tatsu.exceptions import FailedParse
from tqdm import tqdm

from accounts.models import Country
from calendarAPI import settings
from events.models import Event, Notification


def get_official_holidays():

    queryset_country = Country.objects.exclude(country_name=None)
    notification = Notification.objects.get(id=1)
    for country in tqdm(queryset_country):
        url = f"https://www.officeholidays.com/ics/ics_country.php?tbl_country={country}"
        if requests.get(url).status_code != 200:
            continue
        try:
            calendar = Calendar(requests.get(url).text)
        except FailedParse:
            continue
        objs = (Event(
            name=event.name,
            start_datetime=event.begin.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
            end_datetime=event.end.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
            notification=notification,
            country_holiday=country,
            official_holiday=True
            ) for event in calendar.events
        )
        Event.objects.bulk_create(objs)


class Command(BaseCommand):

    def handle(self, *args, **options):
        get_official_holidays()
