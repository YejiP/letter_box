import pika
class Subscriber():
    def subscribe(self,queue_name,job_class):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_consume(queue=queue_name,
                        auto_ack=True,
                        on_message_callback=job_class.perform)
        channel.start_consuming()

"""
separate queue for each job, 
and then pass class as a parameter, and put perform inside all the job class. like an interface
"""