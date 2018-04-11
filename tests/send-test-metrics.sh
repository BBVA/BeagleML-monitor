#!/bin/bash

DOCKER_CONTAINER=tests_kafka_1
KFK_PATH=/opt/kafka_2.11-0.10.1.0/bin
SERVER=localhost:9092
MAIN_TOPIC=experiments
EXPERIMENT_ID=2018122151104215138491FF
METRICS_TOPIC=$EXPERIMENT_ID-metrics
SAMPLE_METRICS_FILE=json_metrics

echo Creating experiement $EXPERIMENT_ID in database ...
./run-query.sh insertExperiment.qry
echo Done

echo Sending metric message to $MAIN_TOPIC ...
echo $METRICS_TOPIC | docker exec -i $DOCKER_CONTAINER \
                          $KFK_PATH/kafka-console-producer.sh --broker-list=$SERVER --topic=$MAIN_TOPIC
echo Done

echo Waiting 10 seconds ...
sleep 10

echo Sending metrics to topic $METRICS_TOPIC ...
cat $SAMPLE_METRICS_FILE| docker exec -i $DOCKER_CONTAINER \
                           $KFK_PATH/kafka-console-producer.sh --broker-list=$SERVER --topic=$METRICS_TOPIC
echo Done
