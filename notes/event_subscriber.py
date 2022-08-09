import pika


class Event_subscriber():
    @classmethod
    def subscribe(self, job_class):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(
            exchange='audit', exchange_type='fanout', durable=True)
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange='audit', queue=queue_name)
        channel.basic_consume(queue=queue_name,
                              on_message_callback=job_class.perform)

        channel.start_consuming()


"""
source ../venv/bin/activate
python manage.py shell_plus
from notes.event_subscriber import Event_subscriber
from notes.audit_job import Audit_job
Event_subscriber.subscribe(Audit_job)


source ../venv/bin/activate
python manage.py shell_plus
from notes.event_subscriber import Event_subscriber
from notes.user_job import User_job
Event_subscriber.subscribe(User_job)
"""
"""
separate queue for each job, 
and then pass class as a parameter, and put perform inside all the job class. like an interface
"""
