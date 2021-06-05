import os, time
import pulsar
import pika
from pymercure.publisher.sync import SyncPublisher
from pymercure.message import Message
from urllib.parse import urlparse

def producer_pulsar():
    uri_parsed = urlparse(os.environ["PULSAR_URL"])
    client = pulsar.Client(
        uri_parsed.scheme + "://" + uri_parsed.netloc,
        authentication=pulsar.AuthenticationToken(str(os.environ["PULSAR_JWT"])),
    )

    producer = client.create_producer(uri_parsed.path[1:])

    i = 0

    while True:
        msg = "test : " + str(i)
        producer.send(msg.encode('utf-8'))
        print("message produce: " + str(i))
        i = i + 1
        time.sleep(10)


def producer_rabbitmq():
    parameters = pika.URLParameters(os.environ["RABBITMQ_URL"])

    connection = pika.BlockingConnection(parameters)

    client = connection.channel()

    i = 0

    while True:
        message = "test : " + str(i)
        
        client.basic_publish('test',
                    'test',
                    message.encode('utf-8'),
                    pika.BasicProperties(content_type='text/plain',
                                        delivery_mode=1))
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

print("start produce message")
locals()["producer_"+os.environ["PRODUCE"]]()
