import datetime

import pytz
from django.core import mail
from django_celery_beat.models import ClockedSchedule
from rest_framework.test import APITestCase
from django.urls import reverse

from accounts.models import Country, CustomUser
from events.models import Notification, Event
from events.tasks import send_event_notification


class TestSendEventNotification(APITestCase):
    def setUp(self):
        country = Country.objects.create(country_name='Afghanistan')
        notification = Notification.objects.create(
            description='Send a message in 6 hours',
            value_time=6)
        user = CustomUser.objects.create(
            username='TestUser_1',
            email='TestUser_1@gmail.com',
            password='user1234',
            country=country,
            is_active=True
        )
        self.client.force_authenticate(user)
        self.client.post(
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

    def test_send_event_notification(self):
        email = CustomUser.objects.get(pk=1).email
        event = Event.objects.get(pk=1)
        event_name = event.name
        event_start_datetime = event.start_datetime
        clocked_id = ClockedSchedule.objects.get(pk=1).id
        send_event_notification(clocked_id, email, event_start_datetime, event_name)
        soup = mail.outbox[0]
        self.assertTrue(soup)
        email_from = soup.from_email
        self.assertEqual(email_from, 'TestUser24071987@gmail.com')
        email_to = soup.to
        self.assertEqual(email_to, ['TestUser_1@gmail.com'])
        message = soup.body
        self.assertEqual(message, 'Your event Go to swimming pool will be start 2022-09-23 12:00:00+00:00.')
        clocked_id = ClockedSchedule.objects.all()
        self.assertFalse(clocked_id)
        subject = soup.subject
        self.assertEqual(subject, 'Upcoming event')
