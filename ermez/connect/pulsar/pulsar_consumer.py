import pulsar
from urllib.parse import urlparse, parse_qs
from ermez.connect.abstract_consumer import AbstractConsumer


class Consumer(AbstractConsumer):
    def __init__(self, uri: str, credential):
        uri_parsed = urlparse(uri)
        query = parse_qs(uri_parsed.query)

        self.client = pulsar.Client(
            uri_parsed.scheme + "://" + uri_parsed.netloc,
            authentication=pulsar.AuthenticationToken(str(credential)),
        )

        self.consumer = self.client.subscribe(query["topic"][0], query["topic"][0])

    def get_message(self):
        while True:
            msg = self.consumer.receive()
            yield msg.data()
