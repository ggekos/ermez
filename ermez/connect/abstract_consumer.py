from abc import ABC, abstractmethod


class AbstractConsumer(ABC):
    @abstractmethod
    def get_message(self):
        pass