import sseclient, requests
from urllib.parse import urlparse, parse_qs


class Consumer:
    def __init__(self, uri: str, credential):
        self.uri_parsed = urlparse(uri)

        headers = {
            "Accept": "text/event-stream",
            "Authorization": str.encode("Bearer " + credential),
        }

        query = parse_qs(self.uri_parsed.query)

        response = requests.get(
            self.uri_parsed.scheme + "://" + self.uri_parsed.netloc + self.uri_parsed.path,
            stream=True,
            headers=headers,
            params={"topic": [query["topic"][0]]},
        )
        self.client = sseclient.SSEClient(response)

    def get_message(self):
        for event in self.client.events():
            yield event.data