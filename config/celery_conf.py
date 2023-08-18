import os
from celery import Celery
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

celery_app = Celery('config')

celery_app.autodiscover_tasks()

celery_app.conf.broker_url = 'amqp://admin:1234@localhost:5672//'
celery_app.conf.result_backend = 'rpc://'
celery_app.conf.task_serializer = 'json'
celery_app.conf.result_serializer = 'pickle'
celery_app.conf.accept_content = ['json', 'pickle']
celery_app.conf.result_expires = timedelta(days=1)
celery_app.conf.task_always_eager = False  # should client wait to task become completed ?
celery_app.conf.worker_prefetch_multiplier = 4  # on heavier task user 1 worker per task
