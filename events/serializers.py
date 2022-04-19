from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from events.models import Event


class ListCreateApiEventSerializer(ModelSerializer):
    class Meta:
        model = Event
        exclude = ["user", "country_holiday", "official_holiday"]

    def validate(self, attrs):
        start_datetime = self.initial_data["start_datetime"]
        end_date = self.initial_data["end_datetime"]
        if end_date:
            if start_datetime >= end_date:
                raise ValidationError({
                    "detail": "Please, enter a valid end time for the event"
                }, code='invalid')
        return attrs
