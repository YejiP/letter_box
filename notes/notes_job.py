import json
from .models import Notes
class NotesJob:
    def perform(ch, method, properties, body):
        message=json.loads(body)
        Notes.objects.create(user_id =message['user_id'], title = message['title'], text =message['text']) 