from abc import ABC, abstractmethod


class AbstractProducer(ABC):
    @abstractmethod
    def publish_message(self):
        pass