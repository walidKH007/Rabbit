#!/usr/bin/python
import pika
connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.101'))
channel = connection.channel()
channel.queue_declare(queue='M1RT-DAS')
print("the queue create successfully")
connection.close()
