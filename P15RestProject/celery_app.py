import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'P15RestProject.settings')

app = Celery('P15RestProject')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
