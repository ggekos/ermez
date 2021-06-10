import pika
from urllib.parse import urlparse, parse_qs


class Consumer:
    def __init__(self, uri: str, credential):
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

    def get_message(self):
        for body in self.client.consume(self.query["topic"][0]):
            yield str(body)
