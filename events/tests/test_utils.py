import datetime

import pytz
from django.urls import reverse
from django_celery_beat.models import PeriodicTask, ClockedSchedule
from rest_framework.test import APITestCase

from accounts.models import Country, CustomUser
from events.models import Event, Notification
from events.utils.create_tasks import create_task_send_notification


class TestCreateTasks(APITestCase):
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

    def test_create_task_send_notification(self):
        task = PeriodicTask.objects.get(pk=1)

        """Checking if a function creates an object of a class PeriodicTask"""

        self.assertTrue(task)

    def test_datetime_notification_value(self):
        clocked_schedule = ClockedSchedule.objects.get(pk=1)
        datetime_notification = clocked_schedule.clocked_time

        """Checking if we get the expected value for the datetime_notification"""

        self.assertEqual(
            datetime_notification,
            datetime.datetime(2022, 9, 23, 6, 0, tzinfo=pytz.UTC)
        )

    def test_clocked_schedule_value(self):
        clocked_schedule = ClockedSchedule.objects.get(pk=1)
        clocked_time = clocked_schedule.clocked_time

        """Checking if we get the expected value for the clocked_schedule"""

        self.assertEqual(
            clocked_time,
            datetime.datetime(2022, 9, 23, 6, 0, tzinfo=pytz.UTC)
        )

    def test_name_field_content(self):
        task = PeriodicTask.objects.get(pk=1)
        task_name = task.name

        """Checking if we get the expected data for name field"""

        self.assertEqual(
            task_name,
            'send_notification, TestUser_1@gmail.com, Go to swimming pool'
        )

    def test_task_field_content(self):
        task = PeriodicTask.objects.get(pk=1)
        task_task = task.task

        """Checking if we get the expected data for task field"""

        self.assertEqual(
            task_task,
            'events.tasks.send_event_notification'
        )

    def test_clocked_field_content(self):
        clocked = ClockedSchedule.objects.get(pk=1)
        task = PeriodicTask.objects.get(pk=1)
        task_clocked = task.clocked

        """Checking if we get the expected data for clocked field"""

        self.assertEqual(task_clocked, clocked)

    def test_one_off_field_content(self):
        task = PeriodicTask.objects.get(pk=1)
        task_cone_off = task.one_off

        """Checking if we get the expected data for one_off field"""

        self.assertEqual(task_cone_off, True)

    def test_kwargs_field_content(self):
        task = PeriodicTask.objects.get(pk=1)
        task_kwargs = task.kwargs

        """Checking if we get the expected data for kwargs field"""

        self.assertEqual(
            task_kwargs,
            '{"event_name": "Go to swimming pool", "email": "TestUser_1@gmail.com", "clocked_id": 1, '
            '"event_start_datetime": "12:00:00, 23-09-2022"}'
        )
