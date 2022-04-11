from datetime import timedelta
from json import dumps

from django_celery_beat.models import PeriodicTask, ClockedSchedule


def create_task_send_notification(event_name, notification, event_start_datetime, email):

    """Create task for send notification before event. """

    date_time_notification = event_start_datetime - timedelta(hours=notification)
    clocked_schedule = ClockedSchedule.objects.create(clocked_time=date_time_notification)
    PeriodicTask.objects.create(
        name=f"send_notification, {email}, {event_name}",
        task="events.tasks.send_event_notification",
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
