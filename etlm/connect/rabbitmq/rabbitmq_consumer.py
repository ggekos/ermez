import pika
from urllib.parse import urlparse


class Consumer:
    def __init__(self, uri: str, credential):
        parameters = pika.URLParameters(uri)

        connection = pika.BlockingConnection(parameters)

        self.client = connection.channel()

    def get_message(self):
        for body in self.client.consume('test'):
            yield body