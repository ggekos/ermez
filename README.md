# ermez

Ermez is message transfer tool. Configure a topic to consume and another one to publish.
Currently supporting : Pulsar (consume/publish, no tls), Mercure (consume, publish), Rabbitmq (consume, publish), SQS (consume, publish)

### How to use :

```bash
 docker run -e CONNECTION_STRING_FROM=http://mercure_server/.well-known/mercure?topic=test -e CREDENTIALS_FROM=jwt -e CONNECTION_STRING_TO=amqp://guest:guest@rabbit:5672/%2F?topic=topic&exchange=exchange&routing_key=routing_key ggekos/ermez
```

### Connection strings :

Theses connection strings differs from the usual strings used by services.


Mercure : http://mercure_server/.well-known/mercure?topic=test alongside with a jwt

Pulsar : pulsar://pulsar_server:6650?topic=topic alongside with a jwt

Rabbitmq : amqp://guest:guest@rabbit:5672/%2F?topic=topic&exchange=exchange&routing_key=routing_key

SQS : http://sqsserver:9324?queue=default alongside with aws credentials (region_name:X,aws_secret_access_key:Y,aws_access_key_id:Z,use_ssl:True)

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
- Add support for Azure Message Bus
- Option to ack/delete message
