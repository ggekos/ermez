from typing import Union
from urllib.parse import urlparse
from importlib import import_module
import logging
import os


class conn:
    def __init__(self, uri: str, credentials: Union[str, None], type: str) -> None:
        logging.basicConfig(level=os.getenv("LOGLEVEL", "INFO"))

        self.uri = uri
        self.uri_parsed = urlparse(uri)
        self.credentials = credentials
        self.type = type
        self.protocol = self.determine_broker_from_uri()

        logging.info("Starting " + type + " " + self.protocol + " " + self.uri)

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

        logging.info(type + " " + self.protocol + " started")

    def determine_broker_from_uri(self) -> str:
        protocol = self.uri_parsed.scheme

        if len(protocol) == 0 or protocol not in ["http", "pulsar", "amqp"]:
            raise Exception("Connection error")

        if protocol == "http":
            return "mercure"

        if protocol == "amqp":
            return "rabbitmq"

        return protocol

    def get_message(self):
        return self.consumer.get_message()

    def publish_message(self, message):
        return self.producer.publish_message(message)
