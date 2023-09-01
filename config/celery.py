import os
from celery import Celery

# Задаем старндартный модуль настроек Django для прог-ы 'celery'.
os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='config.settings')
app = Celery('config')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()
