#!/bin/bash

DOCKER_CONTAINER=tools_kafka_1
KFK_PATH=/opt/kafka_2.11-0.10.1.0/bin
SERVER=localhost:9092
MAIN_TOPIC=experiments
TIMESTAMP=$(date +%Y%m%d%W%k%M%s)
METRICS_TOPIC=$(date +%Y%m%d%W%k%M%s)-metrics
#2018122251104215138492ff-metrics

echo Sending metric message to $MAIN_TOPIC ...
echo $METRICS_TOPIC | docker exec -i $DOCKER_CONTAINER \
                          $KFK_PATH/kafka-console-producer.sh --broker-list=$SERVER --topic=$MAIN_TOPIC
echo Done

sleep 10

echo Sending metrics to topic $METRICS_TOPIC ...
cat $1 | docker exec -i $DOCKER_CONTAINER \
                           $KFK_PATH/kafka-console-producer.sh --broker-list=$SERVER --topic=$METRICS_TOPIC
echo Done
