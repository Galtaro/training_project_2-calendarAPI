from django.test import TestCase
from rest_framework.exceptions import ValidationError

from events import serializers
from events.models import Event, Notification
from events.serializers import ListCreateApiEventSerializer


class TestListCreateApiEventSerializer(TestCase):
    def setUp(self):
        notification = Notification.objects.get(pk=1)
        self.event_attribute = {
            'name': 'Afghanistan: Eid Al Adha Holiday',
            'start_datetime': "2023-06-30T00:00:00Z",
            'end_datetime': "2023-07-01T00:00:00Z",
            'notification': notification
        }

        self.event = Event.objects.create(**self.event_attribute)
        self.serializer = ListCreateApiEventSerializer(instance=self.event)

    def test_contains_expected_fields(self):
        data = self.serializer.data

        """Checking if the serializer has the exact attributes expected of it"""

        self.assertCountEqual(data.keys(),
                              ['id', 'name', 'start_datetime', 'end_datetime', 'notification']
                              )

    def test_name_field_content(self):
        data = self.serializer.data

        """Checking if the serializer produces the expected data for name field"""

        self.assertEqual(data['name'], self.event_attribute['name'])

    def test_start_date_field_content(self):
        data = self.serializer.data

        """Checking if the serializer produces the expected data for start_date field"""

        self.assertEqual(data['start_datetime'], self.event_attribute['start_datetime'])

    def test_end_date_field_content(self):
        data = self.serializer.data

        """Checking if the serializer produces the expected data for end_date field"""

        self.assertEqual(data['end_datetime'], self.event_attribute['end_datetime'])

    def test_notification_field_content(self):
        data = self.serializer.data

        """Checking if the serializer produces the expected data for notification field"""

        notification = Notification.objects.get(pk=data['notification'])
        self.assertEqual(notification, self.event_attribute['notification'])

    def test_validate(self):
        notification = Notification.objects.get(pk=1)
        self.initial_data = {
            'name': 'Afghanistan: Eid al-Fitr Holiday',
            'start_datetime': "2023-04-24T00:00:00Z",
            'end_datetime': "2023-04-23T00:00:00Z",
            'notification': notification
        }

        """Checking raises ValidationError when fields 'start_datetime' > 'end_datetime' """

        self.assertRaises(
            ValidationError,
            serializers.ListCreateApiEventSerializer.validate,
            self,
            attrs=None
        )
        self.initial_data = {
            'name': 'Afghanistan: Eid al-Fitr Holiday',
            'start_datetime': "2023-04-23T00:00:00Z",
            'end_datetime': "2023-04-23T00:00:00Z",
            'notification': notification
        }

        """Checking raises ValidationError when fields 'start_datetime' == 'end_datetime' """

        self.assertRaises(
            ValidationError,
            serializers.ListCreateApiEventSerializer.validate,
            self,
            attrs=None
        )