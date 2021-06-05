import pulsar
from urllib.parse import urlparse


class Consumer:
    def __init__(self, uri: str, credential):
        uri_parsed = urlparse(uri)

        self.client = pulsar.Client(
            uri_parsed.scheme + "://" + uri_parsed.netloc,
            authentication=pulsar.AuthenticationToken(str(credential)),
        )

        self.consumer = self.client.subscribe(uri_parsed.path[1:], subscription_name=uri_parsed.path[1:])

    def get_message(self):
        while True:
            msg = self.consumer.receive()
            yield msg.data()