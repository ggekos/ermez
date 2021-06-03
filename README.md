# etl-message

docker to consume and publish.
Currently supporting : Pulsar (consume/publish, no tls), Mercure (consume, publish), Rabbitmq

Connexion strings :

Mercure : http://mercure_server/.well-known/mercure?topic=test alongside with a jwt

Pulsar : pulsar://pulsar_server:6650/topic alongside with a jwt

Rabbitmq : amqp://guest:guest@rabbit:5672/%2F

## Dev set up

copy .env.dist into .env. Fill the value with jwt key and token.

> make install

## dev

> make start

> make stop

## test

> make test