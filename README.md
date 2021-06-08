# ermez

Ermez is message transfer tool. Configure a topic to consume and another one to publish.
Currently supporting : Pulsar (consume/publish, no tls), Mercure (consume, publish), Rabbitmq (consumer, publish).

### How to use :

```bash
 docker run -e CONNECTION_STRING_FROM=http://mercure_server/.well-known/mercure?topic=test -e CREDENTIALS_FROM=jwt -e CONNECTION_STRING_TO=amqp://guest:guest@rabbit:5672/%2F?topic=topic&exchange=exchange&routing_key=routing_key ggekos/ermez
```

### Connection strings :

Mercure : http://mercure_server/.well-known/mercure?topic=test alongside with a jwt

Pulsar : pulsar://pulsar_server:6650?topic=topic alongside with a jwt

Rabbitmq : amqp://guest:guest@rabbit:5672/%2F?topic=topic&exchange=exchange&routing_key=routing_key

## Install

copy .env.dist into .env. Fill the value with jwt key and token.

```bash
make install
```

In the docker compose file you can produce dumb message with the producer.
Change the env var of ermez to test configuration.

```bash
make start

make stop
```

## Todo
- Error connection
- Test
- Add support for SQS
- Add support for Azure Message Bus
- Option to ack message
