class conn:
    def __init__(self, uri: str, credentials: str, type: str) -> None:
        self.uri = uri
        self.credentials = credentials
        self.type = type
        self.protocol = self.determine_broker_from_uri()

        print("test connexion for " + self.protocol)

        if self.protocol == "http":
            self.connect_with_http()

        if self.protocol == "pulsar":
            self.connect_with_pulsar()

    def determine_broker_from_uri(self) -> str:
        protocol = self.uri.split(":")

        if len(protocol[0]) == 0 or protocol[0] not in ["http", "pulsar"]:
            raise Exception("Connexion error")

        return protocol[0]

    def connect_with_http(self):
        if self.type == "consumer":
            from etlm.connect.mercure import mercure_consumer

            self.consumer = mercure_consumer.mercure_consumer(
                self.uri, self.credentials
            )

        if self.type == "producer":
            self.producer = None

    def connect_with_pulsar(self):
        if self.type == "consumer":
            from etlm.connect.pulsar import pulsar_consumer

            self.consumer = pulsar_consumer.mercure_consumer(self.uri, self.credentials)

        if self.type == "producer":
            self.producer = None

    def get_message(self):
        return self.consumer.get_message()

    def publish_message(self, message):
        return self.producer.publish_message(message)