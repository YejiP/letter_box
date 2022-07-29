import os

from celery import Celery
from kombu import Queue

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

app = Celery('setup')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.task_default_queue = 'default'
app.conf.task_queues = (
    Queue('notesq', routing_key='notes.create'),
)
task_routes = {
    'notes.tasks.async_note_create': {
        'queue': 'notesq',
        'routing_key': 'notes.create',
    },
}

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
