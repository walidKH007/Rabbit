#!/usr/bin/python

import docker
import os

client = docker.from_env()

def run_container(container_name):
    client.containers.run(container_name,detach=True)
    print(container_name+" is running.")

def list_conteneurs():
    for container in client.containers.list():
        print("Container ID : {}: Status : {}: Name: {}" .format(container.id, container.status, container.name))

def run_container_from_dockerfile(P,fname):
    client.images.build(path=P,tag=fname)

if __name__ == "__main__":
    print("----------- run container ------------")
    print("")
    container_name="rabbitmq"
    run_container(container_name)
    print("")
    print("----------- create from dockerfile ------------")
    print("")
    fname='/dockerfile'
    path = os.path.dirname(fname)
    run_container_from_dockerfile(fname,"apache")
    print("")
    print("----------- List of container running ------------")
    print("")
    list_conteneurs()


