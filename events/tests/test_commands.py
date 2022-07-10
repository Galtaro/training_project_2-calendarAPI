import urllib.request
from zoneinfo import ZoneInfo

import requests
from django.core.management import call_command
from django.db import IntegrityError
from ics import Calendar
from rest_framework import status
from rest_framework.test import APITransactionTestCase
from tatsu.exceptions import FailedParse
from tqdm import tqdm

from accounts.models import Country
from calendarAPI import settings
from events.models import Event, Notification


class TestCreateOfficialHolidays(APITransactionTestCase):
    reset_sequences = True

    def test_remote_url(self):
        call_command('create_country')
        country = Country.objects.get(pk=2)
        status_code = urllib.request.urlopen(
            f'https://www.officeholidays.com/ics/ics_country.php?tbl_country={country}'
        ).getcode()

        """Checking the accessibility of a remote url"""

        self.assertEqual(status_code, status.HTTP_200_OK)

    def test_get_official_holidays(self):
        notification = Notification.objects.create(
            description='Do not deliver notification',
            value_time=None)
        call_command('create_country')
        call_command('create_official_holidays')
        queryset_events = Event.objects.all()

        """Checking the loading and creation of records in the database from a remote url"""

        self.assertTrue(queryset_events)
        country = Country.objects.get(pk=2)
        url = f'https://www.officeholidays.com/ics/ics_country.php?tbl_country={country}'
        calendar = Calendar(requests.get(url).text)
        events = calendar.events
        event = events.pop()
        name = event.name
        start_datetime = event.begin.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE))
        end_datetime = event.end.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE))
        event_db = Event.objects.filter(name=name, start_datetime=start_datetime, end_datetime=end_datetime)

        """Checking the correct creation of a record in the database with the correct data in the fields"""

        self.assertTrue(event_db)
        queryset_events = list(queryset_events)
        Event.objects.all().delete()
        queryset_country = Country.objects.exclude(country_name=None)
        for country in tqdm(queryset_country):
            url = f'https://www.officeholidays.com/ics/ics_country.php?tbl_country={country}'
            if requests.get(url).status_code != 200:
                continue
            try:
                calendar = Calendar(requests.get(url).text)
            except FailedParse:
                continue
            for event in calendar.events:
                try:
                    Event.objects.create(
                        name=event.name,
                        start_datetime=event.begin.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
                        end_datetime=event.end.datetime.replace(tzinfo=ZoneInfo(settings.TIME_ZONE)),
                        notification=notification,
                        country_holiday=country,
                        official_holiday=True
                    )
                except IntegrityError:
                    continue
        test_queryset_events = Event.objects.all()
        test_queryset_events = list(test_queryset_events)

        """Checking the loading and creation of all records in the database from a remote url"""

        self.assertEqual(len(queryset_events), len(test_queryset_events))

