import boto3
from urllib.parse import urlparse, parse_qs
from ermez.connect.abstract_consumer import AbstractConsumer


class Consumer(AbstractConsumer):
    def __init__(self, uri: str, credential):
        self.uri_parsed = urlparse(uri)
        self.query = parse_qs(self.uri_parsed.query)
        crendentials = credential.split(",")
        credentials_dict = {}
        for credential in crendentials:
            credentials_dict[credential.split(":")[0]] = credential.split(":")[1]

        resource = boto3.resource(
            "sqs",
            endpoint_url=self.uri_parsed.scheme + "://" + self.uri_parsed.netloc,
            region_name=credentials_dict["region_name"],
            aws_secret_access_key=credentials_dict["aws_secret_access_key"],
            aws_access_key_id=credentials_dict["aws_access_key_id"],
            use_ssl=credentials_dict["aws_access_key_id"] == "true",
        )

        self.client = resource.meta.client
        self.queue_url = self.client.get_queue_url(QueueName=self.query["queue"][0])

    def get_message(self):
        while True:
            response = self.client.receive_message(
                QueueUrl=self.queue_url["QueueUrl"],
                AttributeNames=["All"],
                MaxNumberOfMessages=1,
                MessageAttributeNames=["All"],
                WaitTimeSeconds=20,
            )

            message = response["Messages"][0]
            receipt_handle = message["ReceiptHandle"]

            self.client.delete_message(
                QueueUrl=self.queue_url["QueueUrl"], ReceiptHandle=receipt_handle
            )

            yield str(message)
