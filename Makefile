include .env
export $(shell sed 's/=.*//' .env)

ifeq (start,$(firstword $(MAKECMDGOALS)))
	PRODUCER := $(word 2, $(MAKECMDGOALS) )
	CONSUMER := $(word 3, $(MAKECMDGOALS) )
endif

.phony: install start stop test

install:
	echo $$(grep PULSAR_JWT_KEY .env | cut -d '=' -f 2-) | tr -d '\n' > pulsar/conf/my-secret.key

# call with make start from to
start:
	@echo "producer : $(PRODUCER), consumer : $(CONSUMER) "

	sed -i '/SQS_SERVER_REPLICAS/d' .env
	echo "SQS_SERVER_REPLICAS=0" >> .env

	sed -i '/MERCURE_SERVER_REPLICAS/d' .env
	echo "MERCURE_SERVER_REPLICAS=0" >> .env

	sed -i '/PULSAR_SERVER_REPLICAS/d' .env
	echo "PULSAR_SERVER_REPLICAS=0" >> .env

	sed -i '/RABBITMQ_SERVER_REPLICAS/d' .env
	echo "RABBITMQ_SERVER_REPLICAS=0" >> .env

	sed -i '/CONNECTION_STRING_FROM/d' .env
	sed -i '/CREDENTIALS_FROM/d' .env
	sed -i '/CONNECTION_STRING_TO/d' .env
	sed -i '/CREDENTIALS_TO/d' .env

ifeq (sqs, $(CONSUMER))
	sed -i '/PRODUCE/d' .env
	echo "PRODUCE=sqs" >> .env
	sed -i '/SQS_SERVER_REPLICAS/d' .env
	echo "SQS_SERVER_REPLICAS=1" >> .env
	echo "CONNECTION_STRING_FROM=$$SQS_URL" >> .env
endif

ifeq (mercure, $(CONSUMER))
	sed -i '/PRODUCE/d' .env
	echo "PRODUCE=mercure" >> .env
	sed -i '/MERCURE_SERVER_REPLICAS/d' .env
	echo "MERCURE_SERVER_REPLICAS=1" >> .env
	echo "CONNECTION_STRING_FROM=$$MERCURE_URL" >> .env
	echo "CREDENTIALS_FROM=$$MERCURE_JWT" >> .env
endif

ifeq (pulsar, $(CONSUMER))
	sed -i '/PRODUCE/d' .env
	echo "PRODUCE=pulsar" >> .env
	sed -i '/PULSAR_SERVER_REPLICAS/d' .env
	echo "PULSAR_SERVER_REPLICAS=1" >> .env
	echo "CONNECTION_STRING_FROM=$$PULSAR_URL" >> .env
	echo "CREDENTIALS_FROM=$$PULSAR_JWT" >> .env
endif

ifeq (rabbitmq, $(CONSUMER))
	sed -i '/PRODUCE/d' .env
	echo "PRODUCE=rabbitmq" >> .env
	sed -i '/RABBITMQ_SERVER_REPLICAS/d' .env
	echo "RABBITMQ_SERVER_REPLICAS=1" >> .env
	echo "CONNECTION_STRING_FROM=$$RABBITMQ_URL" >> .env
endif

ifeq (sqs, $(PRODUCER))
	sed -i '/SQS_SERVER_REPLICAS/d' .env
	echo "SQS_SERVER_REPLICAS=1" >> .env
	echo "CONNECTION_STRING_TO=$$SQS_URL" >> .env
endif

ifeq (mercure, $(PRODUCER))
	sed -i '/MERCURE_SERVER_REPLICAS/d' .env
	echo "MERCURE_SERVER_REPLICAS=1" >> .env
	echo "CONNECTION_STRING_TO=$$MERCURE_URL" >> .env
	echo "CREDENTIALS_TO=$$MERCURE_JWT" >> .env
endif

ifeq (pulsar, $(PRODUCER))
	sed -i '/PULSAR_SERVER_REPLICAS/d' .env
	echo "PULSAR_SERVER_REPLICAS=1" >> .env
	echo "CONNECTION_STRING_TO=$$PULSAR_URL" >> .env
	echo "CREDENTIALS_TO=$$PULSAR_JWT" >> .env
endif

ifeq (rabbitmq, $(PRODUCER))
	sed -i '/RABBITMQ_SERVER_REPLICAS/d' .env
	echo "RABBITMQ_SERVER_REPLICAS=1" >> .env
	echo "CONNECTION_STRING_TO=$$RABBITMQ_URL" >> .env
endif

	sleep 1

	docker-compose --env-file .env build
	docker-compose --env-file .env up

stop:
	docker-compose --env-file .env down

test:
	