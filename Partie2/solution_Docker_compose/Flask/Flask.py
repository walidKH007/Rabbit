#! /usr/bin/python3
import pika,json,sys,os
from flask import Flask, request, jsonify

app = Flask(__name__)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.101'))
channel = connection.channel()

############ CRUD #################
def create(file):
    channel.queue_delete(queue=file)
    channel.queue_declare(queue=file)
    return True

def write(msg,file):
    channel.basic_publish(exchange='', routing_key=file, body=json.dumps(msg))
    return True


def read(file):
    def callback(ch, method, properties, body):
        data=json.loads(body)
        print(" [x] Received %r" % data)
    channel.basic_consume(queue=file, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def get_file(file):

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
@app.route('/rabbit/create/<file_name>',  methods=['GET','POST'])
def create_queue(file_name=None):
    
    #value = request.args.get('file_name')

    if create(file_name):
        return "Creation de la "+file_name+" termine"

    else:
        return "Erreur creation de la "+file_name
        
##########################################################
@app.route('/rabbit/get_queue/<file_name>',  methods=['GET'])
def get_queue(file_name=None):

    return get_file(file_name)
    
    

################### write Queue #######################
@app.route('/rabbit/<file_name>',  methods=['POST'])
def sender(file_name=None):
    #msg = json.loads(request.form["data"])

    value = json.loads(request.form["data"])
    
    if write(value,file_name):
        return jsonify({"file_name":file_name,"msg":value})
    else:
        return jsonify({"EROR":"Erreur creation de file"})

################### read Queue #######################
@app.route('/rabbit/<file_name>',  methods=['GET'])
def read_queue(file_name=None):
    return read(file_name)

if __name__ == "__main__":
    
    # Test de connexion à la file Rabbitmq
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='192.168.56.101'))
        connection.close()
    except pika.exceptions.AMQPConnectionError:
        print("Erreur : connexion impossible a la file RabbitMq ")
        exit(1)
    
    app.run(host='0.0.0.0', port=5000,debug=True)