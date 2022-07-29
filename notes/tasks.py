from .models import Notes
from celery import shared_task


@shared_task(queue="notesq", routing_key="notes.create")
def async_note_create(data):
    # bulk way
    user_id = 1
    Notes.objects.create(
        user_id=user_id, title=data['title'], text=data['text'])


"""
form -> load balancer -> server request -> run code in server (create sql message to the queue) 
-> queue -> worker process message -> create sql records
"""
