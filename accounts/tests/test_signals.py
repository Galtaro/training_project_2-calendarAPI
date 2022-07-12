import datetime

import pytz
from django.test import TestCase
from bs4 import BeautifulSoup
from django.core import mail
from django.core.management import call_command
from django.db.models import Q
from django.test import TransactionTestCase
from djoser.signals import user_activated

from accounts.models import CustomUser, Country
from events.models import Event, CustomUserEvent, Notification


class TestSendSignal(TestCase):

    def setUp(self):
        Country.objects.create(country_name=None)
        Country.objects.create(country_name='Afghanistan')
        Country.objects.create(country_name='Algeria')
        self.client.post(
            'http://localhost:8000/auth/users/', {
                'username': 'TestUser_1',
                'email': 'TestUser_1@gmail.com',
                'password': 'user1234',
                'country': 2
            }
        )
        self.client.post(
            'http://localhost:8000/auth/users/', {
                'username': 'TestUser_2',
                'email': 'TestUser_2@gmail.com',
                'password': 'user1234',
                'country': 1
            }
        )

    def test_should_send_signal_when_user_activated(self):
        self.signal_was_called = False

        def handler(sender, **kwargs):
            self.signal_was_called = True

        user_activated.connect(handler)
        soup = BeautifulSoup(mail.outbox[0].html, features="lxml")
        href = soup.find('a').get('href')
        token = href.split('/')[-1]
        uid = href.split('/')[-2]
        self.client.get(
            href,
            {"uid": uid, "token": token}
        )
        self.assertTrue(self.signal_was_called)
        user_activated.disconnect(handler)

    def test_should_not_send_signal_when_user_deactivated(self):
        self.signal_was_called = False

        def handler(sender, **kwargs):
            self.signal_was_called = True

        user_activated.connect(handler)

        self.client.post(
            'http://localhost:8000/auth/users/', {
                'username': 'TestUser_3',
                'email': 'TestUser_3@gmail.com',
                'password': 'user1234',
                'country': 3
            }
        )

        self.assertFalse(self.signal_was_called)
        user_activated.disconnect(handler)


class TestSignal(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        Country.objects.create(country_name='None')
        country = Country.objects.create(country_name='Afghanistan')
        notification = Notification.objects.create(
            description='Do not deliver notification'
        )
        Event.objects.create(
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
            notification=notification,
            country_holiday=country,
            official_holiday=True
        )
        Event.objects.create(
            name='Afghanistan: Eid al-Fitr Holiday',
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
                day=24,
                hour=3,
                minute=0,
                tzinfo=pytz.UTC
            ),
            notification=notification,
            country_holiday=country,
            official_holiday=True
        )
        self.client.post(
            'http://localhost:8000/auth/users/', {
                'username': 'TestUser_1',
                'email': 'TestUser_1@gmail.com',
                'password': 'user1234',
                'country': 2
            }
        )
        self.client.post(
            'http://localhost:8000/auth/users/', {
                'username': 'TestUser_2',
                'email': 'TestUser_2@gmail.com',
                'password': 'user1234',
                'country': 1
            }
        )

    def test_add_official_holidays_to_custom_user_with_indicating_country(self):
        soup = BeautifulSoup(mail.outbox[0].html, features="lxml")
        href = soup.find('a').get('href')
        token = href.split('/')[-1]
        uid = href.split('/')[-2]
        self.client.get(
            href,
            {"uid": uid, "token": token}
        )
        user = CustomUser.objects.get(username='TestUser_1')
        country_official_holidays = Event.objects.filter(country_holiday=user.country, official_holiday=True)
        user_official_holidays = Event.objects.filter(
            Q(country_holiday=user.country, official_holiday=True) &
            Q(event_user_event__in=CustomUserEvent.objects.filter(user_id=user.id))
        )
        self.assertQuerysetEqual(country_official_holidays, user_official_holidays, ordered=False)

    def test_add_official_holidays_to_custom_user_without_indicating_country(self):
        soup = BeautifulSoup(mail.outbox[1].html, features="lxml")
        href = soup.find('a').get('href')
        token = href.split('/')[-1]
        uid = href.split('/')[-2]
        self.client.get(
            href,
            {"uid": uid, "token": token}
        )
        user = CustomUser.objects.get(username='TestUser_2')
        user_official_holidays = Event.objects.filter(
            Q(country_holiday=user.country, official_holiday=True) &
            Q(event_user_event__in=CustomUserEvent.objects.filter(user_id=user.id))
        )
        self.assertFalse(user_official_holidays)
