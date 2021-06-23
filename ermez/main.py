import os, time
import logging
from ermez.connect import conn

logging.basicConfig(level=os.getenv("LOGLEVEL", "INFO"))

logging.info("Init consumer")
consumer = conn.conn(
    os.getenv("CONNECTION_STRING_FROM"), os.getenv("CREDENTIALS_FROM", None), "consumer"
)
time.sleep(1)

logging.info("Init producer")
producer = conn.conn(
    os.getenv("CONNECTION_STRING_TO"), os.getenv("CREDENTIALS_TO", None), "producer"
)
time.sleep(1)

for message in consumer.get_message():
    logging.info("Got message")
    producer.publish_message(message)
    logging.info("Message published")
