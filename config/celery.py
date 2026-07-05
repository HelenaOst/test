import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('settings')
app.config_from_object('django.conf:settings', namespace='CELERY')