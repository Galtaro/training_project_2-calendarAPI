import datetime

import pytz
from django.test import TestCase

from accounts.models import CustomUser, Country
from events.models import Event, Notification


class TestEvent(TestCase):

    def test_save(self):
        country = Country.objects.create(country_name='Afghanistan')
        user = CustomUser.objects.create(
            username='TestUser_1',
            email='TestUser_1@gmail.com',
            password='user1234',
            country=country,
            is_active=True
        )
        event = Event.objects.create(
            name='Go to swimming pool',
            start_datetime=datetime.datetime(
                year=2022,
                month=9,
                day=23,
                hour=3,
                minute=0,
                tzinfo=pytz.UTC
            )
        )
        event.user.add(user)
        event_end_datetime = Event.objects.get(pk=1).end_datetime

        """Checking event creation when missing 'end_datetime' field during initialization"""

        self.assertEqual(
            event_end_datetime,
            datetime.datetime(2022, 9, 23, 23, 59, tzinfo=pytz.UTC)
        )


class TestNotification(TestCase):
    def test_string_representation_of_the_notification_instance(self):
        notification = Notification.objects.get(pk=1)

        """Checking string representation of the notification instance when 'value_time' is None"""

        self.assertEqual(str(notification), '---')
