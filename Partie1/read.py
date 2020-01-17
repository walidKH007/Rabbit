#!/usr/bin/python
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.101'))
channel = connection.channel()
channel.queue_declare(queue='M1RT-DAS')
def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
channel.basic_consume(
    queue='M1RT-DAS', on_message_callback=callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()