import datetime
import json

import pytz
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from accounts.models import CustomUser, Country
from events.models import Notification, Event, CustomUserEvent


class TestListCreateApiEvent(APITestCase):
    def setUp(self):
        country_1 = Country.objects.create(country_name=None)
        country_2 = Country.objects.create(country_name='Afghanistan')
        notification = Notification.objects.create(
            description='Send a message in 6 hours',
            value_time=6)
        event_1 = Event.objects.create(
            name='Afghanistan: Eid Al Adha Holiday',
            start_datetime=datetime.datetime(
                year=2023,
                month=6,
                day=30,
                hour=3,
                minute=0,
                tzinfo=pytz.UTC
            ),
            end_datetime=datetime.datetime(
                year=2023,
                month=7,
                day=1,
                hour=3,
                minute=0,
                tzinfo=pytz.UTC
            ),
            country_holiday=country_2,
            official_holiday=True
        )
        event_2 = Event.objects.create(
            name='Go to jogging',
            start_datetime=datetime.datetime(
                year=2023,
                month=4,
                day=23,
                hour=3,
                minute=0,
                tzinfo=pytz.UTC
            ),
            end_datetime=datetime.datetime(
                year=2023,
                month=4,
                day=23,
                hour=6,
                minute=0,
                tzinfo=pytz.UTC
            ),
            notification=notification,
        )
        event_3 = Event.objects.create(
            name='Go to cycling',
            start_datetime=datetime.datetime(
                year=2023,
                month=4,
                day=23,
                hour=3,
                minute=0,
                tzinfo=pytz.UTC
            ),
            end_datetime=datetime.datetime(
                year=2023,
                month=4,
                day=23,
                hour=6,
                minute=0,
                tzinfo=pytz.UTC
            ),
            notification=notification,
        )
        user_1 = CustomUser.objects.create(
            username='TestUser_1',
            email='TestUser_1@gmail.com',
            password='user1234',
            country=country_1,
            is_active=True
        )
        user_2 = CustomUser.objects.create(
            username='TestUser_2',
            email='TestUser_2@gmail.com',
            password='user1234',
            country=country_2,
            is_active=True
        )
        CustomUserEvent.objects.create(user=user_2, event=event_1)
        CustomUserEvent.objects.create(user=user_2, event=event_2)
        CustomUserEvent.objects.create(user=user_1, event=event_3)

    def test_post_with_authenticate(self):
        user = CustomUser.objects.get(pk=1)
        notification = Notification.objects.get(pk=1)
        self.client.force_authenticate(user)
        response = self.client.post(
            reverse('Event:list-create-event'),
            data={
                'name': 'Go to swimming pool',
                'start_datetime': datetime.datetime(
                    year=2022,
                    month=9,
                    day=23,
                    hour=12,
                    minute=0,
                    tzinfo=pytz.UTC),
                'end_datetime': datetime.datetime(
                    year=2022,
                    month=9,
                    day=23,
                    hour=18,
                    minute=0,
                    tzinfo=pytz.UTC),
                'notification': notification.pk
            }
        )

        """Checking post response status code with authenticate"""

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_without_authenticate(self):
        response = self.client.post(
            reverse('Event:list-create-event')
        )

        """Checking post response status code without authenticate"""

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_with_authenticate(self):
        user = CustomUser.objects.get(pk=1)
        self.client.force_authenticate(user)
        response = self.client.get(
            reverse('Event:list-create-event')
        )

        """Checking get response status code with authenticate"""

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_without_authenticate(self):
        response = self.client.get(
            reverse('Event:list-create-event')
        )

        """Checking get response status code without authenticate"""

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_list_event_user_without_country(self):
        user = CustomUser.objects.get(pk=1)
        self.client.force_authenticate(user)
        response = self.client.get(
            reverse('Event:list-create-event')
        )
        json_response_content = json.loads(response.content)

        """Checking list event user without country"""

        self.assertEqual(
            json_response_content, [
                {'id': 3,
                 'name': 'Go to cycling',
                 'start_datetime': '2023-04-23T03:00:00Z',
                 'end_datetime': '2023-04-23T06:00:00Z',
                 'notification': 2}
            ]
        )

    def test_get_list_event_user_with_country(self):
        user = CustomUser.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            reverse('Event:list-create-event')
        )
        json_response_content = json.loads(response.content)

        """Checking list event user with country"""

        self.assertEqual(
            json_response_content, [
                {'id': 1,
                 'name': 'Afghanistan: Eid Al Adha Holiday',
                 'start_datetime': '2023-06-30T03:00:00Z',
                 'end_datetime': '2023-07-01T03:00:00Z',
                 'notification': 1
                 },
                {'id': 2,
                 'name': 'Go to jogging',
                 'start_datetime': '2023-04-23T03:00:00Z',
                 'end_datetime': '2023-04-23T06:00:00Z',
                 'notification': 2
                 }
            ]
        )

    def test_create_event_and_tusk_if_notification_true(self):
        user = CustomUser.objects.get(pk=2)
        notification = Notification.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.post(
            reverse('Event:list-create-event'),
            data={
                'name': 'Go to swimming pool',
                'start_datetime': datetime.datetime(
                    year=2022,
                    month=9,
                    day=23,
                    hour=12,
                    minute=0,
                    tzinfo=pytz.UTC),
                'end_datetime': datetime.datetime(
                    year=2022,
                    month=9,
                    day=23,
                    hour=18,
                    minute=0,
                    tzinfo=pytz.UTC),
                'notification': notification.pk
            }
        )

        """Checking create event and create tusk if notification is true"""

        self.assertEqual(
            response.data, (
                {'event_name': 'Go to swimming pool',
                 'datetime_notification': datetime.datetime(2022, 9, 23, 6, 0, tzinfo=pytz.UTC)},
                {'id': 4, 'name': 'Go to swimming pool', 'start_datetime': '2022-09-23T12:00:00Z',
                 'end_datetime': '2022-09-23T18:00:00Z', 'notification': 2}
            )
        )

    def test_create_event_and_tusk_if_notification_false(self):
        user = CustomUser.objects.get(pk=2)
        notification = Notification.objects.get(pk=1)
        self.client.force_authenticate(user)
        response = self.client.post(
            reverse('Event:list-create-event'),
            data={
                'name': 'Go to swimming pool',
                'start_datetime': datetime.datetime(
                    year=2022,
                    month=9,
                    day=23,
                    hour=12,
                    minute=0,
                    tzinfo=pytz.UTC),
                'end_datetime': datetime.datetime(
                    year=2022,
                    month=9,
                    day=23,
                    hour=18,
                    minute=0,
                    tzinfo=pytz.UTC),
                'notification': notification.pk
            }
        )

        """Checking create event and create tusk if notification is false"""

        self.assertEqual(
            response.data, (
                {'id': 4, 'name': 'Go to swimming pool',
                 'start_datetime': '2022-09-23T12:00:00Z',
                 'end_datetime': '2022-09-23T18:00:00Z',
                 'notification': 1}
            )
        )

    def test_get_list_with_filter_official_holiday_false(self):
        user = CustomUser.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            reverse('Event:list-create-event'),
            data={'official_holiday': False}
        )
        json_response_content = json.loads(response.content)

        """Checking get list with filter when 'official holiday' is false"""

        self.assertEqual(
            json_response_content, [
                {'id': 2,
                 'name': 'Go to jogging',
                 'start_datetime': '2023-04-23T03:00:00Z',
                 'end_datetime': '2023-04-23T06:00:00Z',
                 'notification': 2}
            ]
        )

    def test_get_list_with_filter_official_holiday_true(self):
        user = CustomUser.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            reverse('Event:list-create-event'),
            data={'official_holiday': True}
        )
        json_response_content = json.loads(response.content)

        """Checking get list with filter when 'official holiday' is true"""

        self.assertEqual(
            json_response_content, [
                {'id': 1,
                 'name': 'Afghanistan: Eid Al Adha Holiday',
                 'start_datetime': '2023-06-30T03:00:00Z',
                 'end_datetime': '2023-07-01T03:00:00Z',
                 'notification': 1}
            ]
        )

    def test_get_list_with_filter_from_datetime(self):
        user = CustomUser.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            reverse('Event:list-create-event'),
            data={'from_datetime': '2023-06-29T03:00:00Z'}
        )
        json_response_content = json.loads(response.content)

        """Checking get list with filter when 'from datetime' indicated"""

        self.assertEqual(
            json_response_content, [
                {'id': 1,
                 'name': 'Afghanistan: Eid Al Adha Holiday',
                 'start_datetime': '2023-06-30T03:00:00Z',
                 'end_datetime': '2023-07-01T03:00:00Z',
                 'notification': 1}
            ]
        )

    def test_get_list_with_filter_to_datetime(self):
        user = CustomUser.objects.get(pk=2)
        self.client.force_authenticate(user)
        response = self.client.get(
            reverse('Event:list-create-event'),
            data={'to_datetime': '2023-04-27T06:00:00Z'}
        )
        json_response_content = json.loads(response.content)

        """Checking get list with filter when 'to datetime' indicated"""

        self.assertEqual(
            json_response_content, [
                {'id': 2,
                 'name': 'Go to jogging',
                 'start_datetime': '2023-04-23T03:00:00Z',
                 'end_datetime': '2023-04-23T06:00:00Z',
                 'notification': 2}
            ]
        )
