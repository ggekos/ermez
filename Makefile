.phony: install start stop test

install:
	echo $$(grep PULSAR_JWT_KEY .env | cut -d '=' -f 2-) | tr -d '\n' > pulsar/conf/my-secret.key

start:
	docker-compose --env-file .env build
	docker-compose --env-file .env up

stop:
	docker-compose --env-file .env down

test:
	