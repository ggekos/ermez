import pulsar
from urllib.parse import urlparse, parse_qs
from ermez.connect.abstract_producer import AbstractProducer


class Producer(AbstractProducer):
    def __init__(self, uri: str, credential: str):
        uri_parsed = urlparse(uri)
        query = parse_qs(uri_parsed.query)

        self.client = pulsar.Client(
            uri_parsed.scheme + "://" + uri_parsed.netloc,
            authentication=pulsar.AuthenticationToken(str(credential)),
        )

        self.producer = self.client.create_producer(query["topic"][0])

    def publish_message(self, message):
        self.producer.send(message.encode("utf-8"))
