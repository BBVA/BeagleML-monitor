#/bin/bash

TESTS_PATH=/opt/tests
CONTAINER_NAME=tests_mongo_1

docker exec -i $CONTAINER_NAME $TESTS_PATH/query.sh $TESTS_PATH/$1
