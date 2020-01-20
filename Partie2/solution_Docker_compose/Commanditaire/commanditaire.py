#!/usr/bin/python

import requests,json,os,pika,sys
from flask import Flask, request, jsonify

app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.101'))
channel = connection.channel()

def create_file(file):
    r = requests.post("http://192.168.56.101:5000/rabbit/create/"+file)
    print(r.text)

def write(msg,file):
    param = {"data" : msg}
    r = requests.post("http://192.168.56.101:5000/rabbit/"+file, data=param)
    print(r.text)


def read_file(file):
    def callback(ch, method, properties, body):
           
        data=json.loads(body)
        print(" [x] Received from worker %r" % data)
    channel.basic_consume(queue=file, on_message_callback=callback, auto_ack=True)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

if __name__ == "__main__":
        
    # Test de connexion à la file Rabbitmq
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.101'))
        connection.close()
    except pika.exceptions.AMQPConnectionError:
        print("Erreur : connexion impossible a la file RabbitMq ")
        exit(1)
    
    create_file("ToDo")
    create_file("Done")


    # Génération des taches
    tache = {}
    tache["git"] = "https://github.com/walidKH007/N_queue.git"
    tache["tache_id"] = "5"
    tache["soustache_id"] = "1"
    tache["cmd"] = "python3 N_queue.py 6 5 1"

    write(json.dumps(tache),"ToDo")


    read_file("Done")

    
    