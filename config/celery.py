import os

from celery import Celery

# Встановлюємо змінну середовища для Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Створюємо екземпляр Celery
app = Celery('config')

# Завантажуємо налаштування з Django (префікс CELERY_)
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматично знаходить задачі у всіх додатках
app.autodiscover_tasks()