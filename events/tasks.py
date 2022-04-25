from django.conf import settings
from celery import shared_task
from django.core.mail import send_mail

from django_celery_beat.models import ClockedSchedule

from events.management.commands.create_official_holidays import get_official_holidays


@shared_task
def send_event_notification(clocked_id, email, event_start_datetime, event_name):
    subject = 'Upcoming event'
    message = f'Your event {event_name} will be start {event_start_datetime}.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    ClockedSchedule.objects.get(id=clocked_id).delete()


@shared_task
def update_official_holidays():
    get_official_holidays()
