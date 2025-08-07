#!/usr/bin/env python
import pika
import time


class publish_engine:

    def __init__(self):

        self._messages = 100
        self._message_interval = 1
        self._queue_name = "shovel.queue.static"
        self._connection = None
        self._channel = None

    def make_connection(self):
        credentials = pika.PlainCredentials('admin', 'admin')
        parameters = pika.ConnectionParameters(
            'rabbitmq-192.168.0.100.nip.io',
            5672, '/',
            credentials, socket_timeout=300)
        self._connection = pika.BlockingConnection(parameters)
        print("Connected Successfully !!!")
        return self._connection

    def channel(self):
        self._channel = self._connection.channel()
        print("Channel opened...")

    def declare_queue(self):
        self._channel.queue_declare(queue=self._queue_name, durable=True)
        print("Queue declared....")

    def publish_message(self):
        message_count = 0
        while message_count < self._messages:
            message_count += 1
            message_body = "task number %i" % (message_count)
            self._channel.basic_publish(exchange='',
                                        routing_key=self._queue_name,
                                        body=message_body,
                                        properties=pika.BasicProperties(
                                            delivery_mode=2  # make persistent
                                        ))
            print("Published message %i" % (message_count))
            time.sleep(self._message_interval)

    def close_connection(self):
        self._connection.close()
        print("Closed connection....")

    def run(self):
        self.make_connection()
        self.channel()
        self.declare_queue()
        self.publish_message()
        self.close_connection()


if __name__ == '__main__':
    engine = publish_engine()
    engine.run()
