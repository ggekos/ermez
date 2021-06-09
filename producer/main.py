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
    publisher = SyncPublisher(
        os.environ["MERCURE_URL"],
        os.environ["MERCURE_JWT"],
    )

    i = 0

    while True:
        msg = Message(["test"], "test : " + str(i))
        publisher.publish(msg)
        print("message produce: " + str(i))
        i = i + 1
        time.sleep(10)


def producer_sqs():
    uri_parsed = urlparse(os.environ["SQS_URL"])
    query = parse_qs(uri_parsed.query)

    client = boto3.resource(
        "sqs",
        endpoint_url=uri_parsed.scheme + "://" + uri_parsed.netloc,
        region_name="elasticmq",
        aws_secret_access_key="x",
        aws_access_key_id="x",
        use_ssl=False,
    )

    queue = client.get_queue_by_name(QueueName=query["queue"][0])

    i = 0

    while True:
        queue.send_message(
            DelaySeconds=10,
            MessageAttributes={},
            MessageBody=("message produce: " + str(i)),
        )
        print("message produce: " + str(i))
        i = i + 1
        time.sleep(10)


print("start produce message")
locals()["producer_" + os.environ["PRODUCE"]]()
