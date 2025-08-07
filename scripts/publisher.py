import pika
import os
import logging
logging.basicConfig()

url = os.environ.get('RABBITMQ_URL',
                     'amqp://admin:admin@rabbitmq-192.168.0.100.nip.io/%2f')
# 'amqp://admin:admin@localhost:5672/%2f')
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params)  # Connect to RABBITMQ_URL
channel = connection.channel()  # start a channel
channel.queue_declare(queue='pdfprocess')  # Declare a queue
# send a message

channel.basic_publish(exchange='', routing_key='pdfprocess',
                      body='User information')
print("[x] Message sent to consumer")
connection.close()
