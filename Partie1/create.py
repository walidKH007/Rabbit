#!/usr/bin/python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.101'))
channel = connection.channel()

def create_queue(queue_name):
    channel.queue_declare(queue=queue_name)
    print("the queue create successfully")
    #connection.close()

def read_queue(queue_name):
    channel.queue_declare(queue=queue_name)
    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

def wirte_queue(queue_name,body_msg):
    channel.queue_declare(queue=queue_name)
    channel.basic_publish(exchange='', routing_key=queue_name, body=body_msg)
    print (" Message sent ")
   # connection.close()

if __name__ == "__main__":
    create_queue("Master_DAS")
    wirte_queue("Master_DAS", "Welcome to Master Das")
    read_queue("Master_DAS")