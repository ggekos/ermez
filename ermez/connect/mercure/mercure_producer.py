from pymercure.publisher.sync import SyncPublisher
from pymercure.message import Message
from urllib.parse import urlparse, parse_qs
from ermez.connect.abstract_producer import AbstractProducer


class Producer(AbstractProducer):
    def __init__(self, uri: str, credential: str):
        self.uri_parsed = urlparse(uri)
        self.producer = SyncPublisher(
            self.uri_parsed.scheme
            + "://"
            + self.uri_parsed.netloc
            + self.uri_parsed.path,
            credential,
        )

    def publish_message(self, message):
        query = parse_qs(self.uri_parsed.query)
        msg = Message([query["topic"][0]], str(message))
        self.producer.publish(msg)
