import string
from datetime import timedelta
from json import dumps
import random

from django_celery_beat.models import PeriodicTask, ClockedSchedule


def create_task_send_notification(event_name, notification, event_start_datetime, email):
    """Create task for send notification before event. """

    datetime_notification = event_start_datetime - timedelta(hours=notification)
    clocked_schedule = ClockedSchedule.objects.create(clocked_time=datetime_notification)

    """'PeriodicTask' class field 'name' is unique, so we create a random sequence of 10 ascii characters"""

    letters = string.ascii_lowercase
    random_letters = ''.join(random.choice(letters) for i in range(10))
    PeriodicTask.objects.create(
        name=f'{random_letters}, {email}, {event_name}',
        task='events.tasks.send_event_notification',
        kwargs=dumps(
            {'event_name': event_name,
             'email': email,
             'clocked_id': clocked_schedule.id,
             'event_start_datetime': event_start_datetime.strftime('%H:%M:%S, %d-%m-%Y')
             }
        ),
        clocked=clocked_schedule,
        one_off=True
    )
    return {'event_name': event_name, 'datetime_notification': datetime_notification}
