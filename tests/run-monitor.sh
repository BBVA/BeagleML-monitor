#!/bin/bash

LOG_CONFIG_FILE="logging.yaml"
MAIN_TOPIC="experiments"
KAFKA_SERVERS="tests_kafka_1"
KAFKA_GROUP="mygroup"
MONGO_URL="tests_mongo_1"
MONGODB_USER="userS1H"
MONGODB_PASSWORD="14tHhw1FjcP42Xiy"
MONGODB_DATABASE="modeling"
DOCKER_NETWORK="tests_beagleml"

DOCKER_IMAGE=beagleml-monitor:latest

docker run -d  \
       -e LOG_CONFIG_FILE=$LOG_CONFIG_FILE \
       -e MAIN_TOPIC=$MAIN_TOPIC \
       -e KAFKA_SERVERS=$KAFKA_SERVERS \
       -e KAFKA_GROUP=$KAFKA_GROUP \
       -e MONGO_URL=$MONGO_URL \
       -e MONGODB_USER=$MONGODB_USER \
       -e MONGODB_PASSWORD=$MONGODB_PASSWORD \
       -e MONGODB_DATABASE=$MONGODB_DATABASE \
       --network $DOCKER_NETWORK \
       --name tests_monitor \
       $DOCKER_IMAGE \
       ./start.sh


