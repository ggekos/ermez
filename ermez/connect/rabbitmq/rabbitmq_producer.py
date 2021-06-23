import pika
from urllib.parse import urlparse, parse_qs
from ermez.connect.abstract_producer import AbstractProducer


class Producer(AbstractProducer):
    def __init__(self, uri: str, credential: str):
        self.uri_parsed = urlparse(uri)
        self.query = parse_qs(self.uri_parsed.query)

        parameters = pika.URLParameters(
            self.uri_parsed.scheme
            + "://"
            + self.uri_parsed.netloc
            + self.uri_parsed.path
        )

        connection = pika.BlockingConnection(parameters)

        self.client = connection.channel()

    def publish_message(self, message):
        self.client.basic_publish(
            self.query["exchange"][0],
            self.query["routing_key"][0],
            message.encode("utf-8"),
            pika.BasicProperties(content_type="text/plain", delivery_mode=1),
        )
