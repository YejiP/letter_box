import pika


class Emit_event():
    def publish(message):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(
            exchange='audit', exchange_type='fanout', durable=True)
        channel.basic_publish(exchange='audit', routing_key='', body=message)
        print(" [x] Sent %r" % message)

        connection.close()
