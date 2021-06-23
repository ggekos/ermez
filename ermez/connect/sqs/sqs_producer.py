import boto3
from urllib.parse import urlparse, parse_qs


class Producer:
    def __init__(self, uri: str, credential: str):
        self.uri_parsed = urlparse(uri)
        self.query = parse_qs(self.uri_parsed.query)
        crendentials = credential.split(",")
        credentials_dict = {}
        for credential in crendentials:
            credentials_dict[credential.split(":")[0]] = credential.split(":")[1]

        self.client = boto3.resource(
            "sqs",
            endpoint_url=self.uri_parsed.scheme + "://" + self.uri_parsed.netloc,
            region_name=credentials_dict["region_name"],
            aws_secret_access_key=credentials_dict["aws_secret_access_key"],
            aws_access_key_id=credentials_dict["aws_access_key_id"],
            use_ssl=credentials_dict["aws_access_key_id"] == "true",
        )

        self.queue = self.client.get_queue_by_name(QueueName=self.query["queue"][0])

    def publish_message(self, message):
        self.queue.send_message(
            DelaySeconds=10,
            MessageAttributes={},
            MessageBody=(message),
        )
