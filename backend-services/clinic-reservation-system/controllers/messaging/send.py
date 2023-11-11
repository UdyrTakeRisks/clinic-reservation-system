import json
import pika


def notifyDoctor(doctorID, patientID, operation):

    message = {
        "doctorId": doctorID,
        "patientId": patientID,
        "Operation": operation
    }
    messageBody = json.dumps(message)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='clinic_reservation')

    channel.basic_publish(exchange='',
                          routing_key='clinic_reservation',
                          body=messageBody.encode('utf-8'))


