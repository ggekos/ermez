import os, time
import pulsar
import pika
import boto3
from pymercure.publisher.sync import SyncPublisher
from pymercure.message import Message
from urllib.parse import urlparse, parse_qs


def producer_pulsar():
    uri_parsed = urlparse(os.environ["PULSAR_URL"])
    query = parse_qs(uri_parsed.query)
    client = pulsar.Client(
        uri_parsed.scheme + "://" + uri_parsed.netloc,
        authentication=pulsar.AuthenticationToken(str(os.environ["PULSAR_JWT"])),
    )

    producer = client.create_producer(query["topic"][0])

    i = 0

    while True:
        msg = "test : " + str(i)
        producer.send(msg.encode("utf-8"))
        print("message produce: " + str(i))
        i = i + 1
        time.sleep(10)


def producer_rabbitmq():
    uri_parsed = urlparse(os.environ["RABBITMQ_URL"])
    query = parse_qs(uri_parsed.query)
    parameters = pika.URLParameters(
        uri_parsed.scheme + "://" + uri_parsed.netloc + uri_parsed.path
    )

    connection = pika.BlockingConnection(parameters)

    client = connection.channel()

    i = 0

    while True:
        message = "test : " + str(i)

        client.basic_publish(
            query["exchange"][0],
            query["routing_key"][0],
            message.encode("utf-8"),
            pika.BasicProperties(content_type="text/plain", delivery_mode=1),
        )
        print("message produce: " + str(i))
        i = i + 1
        time.sleep(10)


def producer_mercure():
    uri_parsed = urlparse(os.environ["MERCURE_URL"])

    publisher = SyncPublisher(
        uri_parsed.scheme + "://" + uri_parsed.netloc + uri_parsed.path,
        os.environ["MERCURE_JWT"],
    )

    query = parse_qs(uri_parsed.query)

    i = 0

    while True:
        msg = Message([query["topic"][0]], "test : " + str(i))
        publisher.publish(msg)
        print("message produce: " + str(i))
        i = i + 1
        time.sleep(10)


def producer_sqs():
    uri_parsed = urlparse(os.environ["SQS_URL"])
    query = parse_qs(uri_parsed.query)

    crendentials = (os.environ["SQS_CREDENTIALS"]).split(",")
    credentials_dict = {}
    for credential in crendentials:
        credentials_dict[credential.split(":")[0]] = credential.split(":")[1]

    resource = boto3.resource(
        "sqs",
        endpoint_url=uri_parsed.scheme + "://" + uri_parsed.netloc,
        region_name=credentials_dict["region_name"],
        aws_secret_access_key=credentials_dict["aws_secret_access_key"],
        aws_access_key_id=credentials_dict["aws_access_key_id"],
        use_ssl=credentials_dict["aws_access_key_id"] == "true",
    )
    client = resource.meta.client
    queue_url = client.get_queue_url(QueueName=query["queue"][0])

    i = 0

    while True:
        client.send_message(
            QueueUrl=queue_url["QueueUrl"],
            MessageAttributes={},
            MessageBody=("message produce: " + str(i)),
        )
        print("message produce: " + str(i))
        i = i + 1
        time.sleep(10)


print("start produce message")
locals()["producer_" + os.environ["PRODUCE"]]()
