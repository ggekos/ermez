import pulsar
from urllib.parse import urlparse

class pulsar_producer:
    def __init__(self, uri: str, credential:str):
        uri_parsed = urlparse(uri)

        self.client = pulsar.Client(
            uri_parsed.scheme + "://" + uri_parsed.netloc,
            authentication=pulsar.AuthenticationToken(str(credential)),
        )

        self.producer = self.client.create_producer(uri_parsed.path[1:])

    def publish_message(self, message):
        self.producer.send(message.encode('utf-8'))