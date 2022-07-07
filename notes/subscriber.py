from .serializer import CurrentUserSerializer
from .models import Notes, User
import json
import pika

class Subscriber():
    #receiver should be around here??? in the same function?? then #132 as soon as note is created, it will process 
    #even though notes are still generated.

    def subscribe(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='notes')

            
        def callback(ch, method, properties, body):
            message=json.loads(body)
            print(" [x] Received %r" % body)
            Notes.objects.create(user =User.objects.all().get(id=message['user']['id']), title = message['title'], text =message['text']) 

        channel.basic_consume(queue='notes',
                        auto_ack=True,
                        on_message_callback=callback)
        
        channel.start_consuming()
        
        connection.close()
        print("the end")
