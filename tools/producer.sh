#!/bin/bash

DOCKER_CONTAINER=tools_kafka_1
KFK_PATH=/opt/kafka_2.11-0.10.1.0/bin
SERVER=localhost:9092
TOPIC=experiments

docker exec -ti $DOCKER_CONTAINER $KFK_PATH/kafka-console-producer.sh --broker-list=$SERVER --topic=$TOPIC
