import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


app = Celery()

app.config_from_object("django.conf.settings", namespace="CELERY")
app.conf.result_backend = 'redis://localhost:6379/1'

app.conf.beat_schedule = {
    'handle-scheduled-expenses': {
        'task': 'expenses.tasks.handle_scheduled_transactions',
        'schedule': 30.0,
    },
    'handle-scheduled-incomes': {
        'task': 'incomes.tasks.handle_scheduled_transactions',
        'schedule': 30.0,
    }
}

app.autodiscover_tasks()

