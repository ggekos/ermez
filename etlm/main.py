import os
from etlm.connect import conn

consumer = conn.conn(
    os.getenv("CONNEXION_STRING_FROM"), os.getenv("CREDENTIALS_FROM"), "consumer"
)
producer = conn.conn(
    os.getenv("CONNEXION_STRING_TO"), os.getenv("CREDENTIALS_TO"), "producer"
)

for message in consumer.get_message():
    producer.publish_message(message)
