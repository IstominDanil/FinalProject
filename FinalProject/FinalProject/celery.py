import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FinalProject.settings')

app = Celery('FinalProject')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'send_mail_weekly_mon_8am': {
        'task': 'final.tasks.my_job',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}