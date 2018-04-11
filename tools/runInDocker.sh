#!/bin/bash

LOG_CONFIG_FILE="logging.yaml"
MAIN_TOPIC="experiments"
KAFKA_SERVERS="tools_kafka_1"
KAFKA_GROUP="mygroup"
MONGO_URL="tools_mongo_1"

DOCKER_IMAGE=innotech/beagleml-monitor:0.1.0-8

docker run -ti \
       -e LOG_CONFIG_FILE=$LOG_CONFIG_FILE \
       -e MAIN_TOPIC=$MAIN_TOPIC \
       -e KAFKA_SERVERS=$KAFKA_SERVERS \
       -e KAFKA_GROUP=$KAFKA_GROUP \
       -e MONGO_URL=$MONGO_URL \
       --network tools_beagleml \
       $DOCKER_IMAGE
