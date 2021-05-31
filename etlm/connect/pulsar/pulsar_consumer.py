import pulsar


class pulsar_consumer:
    def __init__(self, uri, credential):
        print("try connecting to ", uri, credential)

        self.client = pulsar.Client(
            uri,
            authentication=pulsar.AuthenticationToken(credential),
        )

    def get_message(self):
        for event in self.client.events():
            yield event.data