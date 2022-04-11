import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calendarAPI.settings')
app = Celery('calendarAPI')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# celery -A calendarAPI worker -l info -P eventlet
# celery -A calendarAPI beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
