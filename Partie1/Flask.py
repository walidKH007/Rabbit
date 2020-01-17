#! /usr/bin/python3
import pika,json,sys,os
from flask import Flask, request, jsonify

app = Flask(__name__)


############ CRUD #################
def create(file):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.101'))
    channel = connection.channel()
    channel.queue_declare(queue=file)
    connection.close()
    return True

def write(msg,file):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.101'))
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key=file, body=json.dumps(msg))
    connection.close()
    return True

def read(file):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.101'))
    channel = connection.channel()
    try:
        method_frame, header_frame, body = channel.basic_get(file)
        if method_frame:
            channel.basic_ack(method_frame.delivery_tag)
            return body
        else:
            return "False"
    except Exception as e:
        return "Erreur"

################### Create Queue #######################
@app.route('/rabbit/',  methods=['POST'])
def create_queue():
   
    value = request.json['file_name']

    if create(value):
        return jsonify({"Message":"Creation de la file termine"})
    else:
        return jsonify({"EROR":"Erreur creation de file"})
    

################### write Queue #######################
@app.route('/rabbit/<file_name>',  methods=['POST'])
def sender(file_name=None):
    #msg = json.loads(request.form["data"])

    msg = request.json['msg']
    
    if write(msg,file_name):
        return jsonify({"file_name":file_name,"msg":msg})
    else:
        return jsonify({"EROR":"Erreur creation de file"})

################### read Queue #######################
@app.route('/rabbit/<file_name>',  methods=['GET'])
def read_queue(file_name=None):
    return read(value)

if __name__ == "__main__":
    
    # Test de connexion à la file Rabbitmq
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.101'))
        connection.close()
    except pika.exceptions.AMQPConnectionError:
        print("Erreur : connexion impossible a la file RabbitMq ")
        exit(1)
    
    app.run(host='0.0.0.0', port=5000,debug=True)