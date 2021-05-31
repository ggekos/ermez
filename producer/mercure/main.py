import os, time
from pymercure.publisher.sync import SyncPublisher
from pymercure.message import Message

publisher = SyncPublisher(
    os.environ["MERCURE_URL"],
    os.environ["MERCURE_JWT"],
)

i = 0

while True:
    msg = Message(["test"], "test : " + str(i))
    publisher.publish(msg)
    i = i + 1
    time.sleep(10)