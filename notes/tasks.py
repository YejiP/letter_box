from .models import Notes
from celery import shared_task


@shared_task
def async_note_create(data):
    #bulk way
    user_id = 3
    Notes.objects.create(user_id=user_id,title = data['title'],text=data['text'])