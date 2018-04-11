#!/bin/bash

LOG_CONFIG_FILE="logging.yaml"
MAIN_TOPIC="experiments"
KAFKA_SERVERS="tools_kafka_1"
KAFKA_GROUP="mygroup"
MONGO_URL="tools_mongo_1"
MONGODB_USER="userS1H"
MONGODB_PASSWORD="14tHhw1FjcP42Xiy"
MONGODB_DATABASE="modeling"
LOCAL_PATH=/home/jeronimogarcia/work/ml/prjs/beagleml-monitor/src

DOCKER_IMAGE=innotech/beagleml-base:0.2.1-4

docker run -ti \
       -e LOG_CONFIG_FILE=$LOG_CONFIG_FILE \
       -e MAIN_TOPIC=$MAIN_TOPIC \
       -e KAFKA_SERVERS=$KAFKA_SERVERS \
       -e KAFKA_GROUP=$KAFKA_GROUP \
       -e MONGO_URL=$MONGO_URL \
       -e MONGODB_USER=$MONGODB_USER \
       -e MONGODB_PASSWORD=$MONGODB_PASSWORD \
       -e MONGODB_DATABASE=$MONGODB_DATABASE \
       -v $LOCAL_PATH:/opt/service \
       -w /opt/service \
       --network tools_beagleml \
       $DOCKER_IMAGE \
       /bin/bash
