from typing import Union
from urllib.parse import urlparse
from importlib import import_module


class conn:
    def __init__(self, uri: str, credentials: Union[str, None], type: str) -> None:
        self.uri = uri
        self.uri_parsed = urlparse(uri)
        self.credentials = credentials
        self.type = type
        self.protocol = self.determine_broker_from_uri()

        if self.type == "consumer":
            consumer = import_module(
                "ermez.connect." + self.protocol + "." + self.protocol + "_consumer"
            )

            self.consumer = consumer.Consumer(self.uri, self.credentials)

        if self.type == "producer":
            producer = import_module(
                "ermez.connect." + self.protocol + "." + self.protocol + "_producer"
            )

            self.producer = producer.Producer(self.uri, self.credentials)

    def determine_broker_from_uri(self) -> str:
        protocol = self.uri_parsed.scheme

        if len(protocol) == 0 or protocol not in ["http", "pulsar", "amqp"]:
            raise Exception("Connection error")

        if protocol == "http":
            protocol = "mercure"

        if protocol == "amqp":
            protocol = "rabbitmq"

        return protocol

    def get_message(self):
        return self.consumer.get_message()

    def publish_message(self, message):
        return self.producer.publish_message(message)
