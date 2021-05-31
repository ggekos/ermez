import sseclient, requests


class mercure_consumer:
    def __init__(self, uri, credential):
        print("try connecting to ", uri, credential)
        headers = {
            "Accept": "text/event-stream",
            "Authorization": str.encode("Bearer " + credential),
        }
        response = requests.get(
            uri,
            stream=True,
            headers=headers,
            params={"topic": ["*"]},
        )
        self.client = sseclient.SSEClient(response)

    def get_message(self):
        for event in self.client.events():
            yield event.data