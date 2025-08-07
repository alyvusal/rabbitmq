import pika
import os
import time


def pdf_process_function(msg):
    print(" PDF processing")
    print(" [x] Received " + str(msg))

    time.sleep(5)  # delays for 5 seconds
    print(" PDF processing finished")
    return


url = os.environ.get('RABBITMQ_URL',
                     'amqp://admin:admin@rabbitmq-192.168.0.100.nip.io/%2f')
#  'amqp://admin:admin@localhost:5672/%2f')
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channel = connection.channel()  # start a channel
channel.queue_declare(queue='pdfprocess')  # Declare a queue


# create a function which is called on incoming messages
def callback(ch, method, properties, body):
    pdf_process_function(body)


# set up subscription on the queue
channel.basic_consume('pdfprocess', callback, auto_ack=True)

# start consuming (blocks)
channel.start_consuming()
connection.close()
