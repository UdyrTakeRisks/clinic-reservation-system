import json
import pika
from os import environ

MQ_HOST = environ.get('MQ_HOST')

print("Rabbit-Mq Host: ", MQ_HOST)

def notifyDoctor(doctorID, patientID, operation):

    message = {
        "doctorId": doctorID,
        "patientId": patientID,
        "Operation": operation
    }
    messageBody = json.dumps(message)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=MQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='clinic_reservation')

    channel.basic_publish(exchange='',
                          routing_key='clinic_reservation',
                          body=messageBody.encode('utf-8'))


