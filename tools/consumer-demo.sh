#!/bin/bash

DOCKER_CONTAINER=deploy_kafka_1
KFK_PATH=/opt/kafka_2.11-0.10.1.0/bin
SERVER=localhost:9092
TOPIC=5a39426d9fcb940006cf99db-metrics

docker exec -ti $DOCKER_CONTAINER  $KFK_PATH/kafka-console-consumer.sh --bootstrap-server=$SERVER --topic=$TOPIC 
