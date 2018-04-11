#!/bin/bash

DOCKER_CONTAINER=tools_kafka_1
KFK_PATH=/opt/kafka_2.11-0.10.1.0/bin
SERVER=localhost:2181

docker exec -ti $DOCKER_CONTAINER watch $KFK_PATH/kafka-topics.sh --zookeeper=$SERVER --list
