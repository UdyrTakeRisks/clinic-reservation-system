import json
import threading

import pika
from flask import jsonify
from os import environ

MQ_HOST = environ.get('MQ_HOST')

print("Rabbit-Mq Host: ", MQ_HOST)

# latestMessage = None
# message_lock = threading.Lock()
#
#
# def fetchDoctorMessages(body):
#     global latestMessage
#     with message_lock:
#         message = json.loads(body)
#         latestMessage = message
#
#
# def getLatestMsg():
#     global latestMessage
#     return jsonify(latestMessage)
#
#
# # def retrieveLatestMsg():
# #     message = getLatestMsg()
# #     if message:
# #         return message
# #     else:  # message = None
# #         return jsonify('No Messages Available')


def getPatientMessages():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=MQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue='clinic_reservation')

    # def callback(ch, method, properties, body):
    #     fetchDoctorMessages(body)
    #
    # channel.basic_consume(queue='clinic_reservation',
    #                       on_message_callback=callback,
    #                       auto_ack=True)
    # waiting for messages
    # channel.start_consuming()
    # Retrieve a single message from the queue
    method_frame, header_frame, body = channel.basic_get(queue='clinic_reservation')

    if method_frame:
        # If a message is received, process it
        message = json.loads(body)
        return message

    connection.close()



