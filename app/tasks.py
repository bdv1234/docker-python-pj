from celery import Celery
from flask import Flask
import os

celery = Celery(__name__)

# Configure broker/backend at import time for Celery worker processes
# (worker doesn't call make_celery, so default to env vars here)
_import_time_broker = (
    os.getenv('CELERY_BROKER_URL')
    or os.getenv('REDIS_URL')
    or 'redis://localhost:6379/0'
)
_import_time_backend = (
    os.getenv('CELERY_RESULT_BACKEND')
    or os.getenv('REDIS_URL')
    or 'redis://localhost:6379/0'
)
celery.conf.broker_url = _import_time_broker
celery.conf.result_backend = _import_time_backend

def make_celery(app: Flask = None):
    broker = (
        (app.config.get('CELERY_BROKER_URL') if app else None)
        or os.getenv('CELERY_BROKER_URL')
        or os.getenv('REDIS_URL')
        or 'redis://localhost:6379/0'
    )
    backend = (
        (app.config.get('CELERY_RESULT_BACKEND') if app else None)
        or os.getenv('CELERY_RESULT_BACKEND')
        or os.getenv('REDIS_URL')
        or 'redis://localhost:6379/0'
    )
    celery.conf.broker_url = broker
    celery.conf.result_backend = backend
    return celery

@celery.task(bind=True)
def create_task_async(self, task_id: int):
    print(f"Background job for task {task_id}")
    return {'task_id': task_id}