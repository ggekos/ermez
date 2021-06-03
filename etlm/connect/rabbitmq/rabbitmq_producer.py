import pika

class Producer:
    def __init__(self, uri: str, credential:str):
        parameters = pika.URLParameters(uri)

        connection = pika.BlockingConnection(parameters)

        self.client = connection.channel()

    def publish_message(self, message):
        self.client.basic_publish('test',
                      'test',
                      message.encode('utf-8'),
                      pika.BasicProperties(content_type='text/plain',
                                           delivery_mode=1))