#!/bin/bash

# start infrastructure
./startup-test.sh

# wait a bit
echo wainting a bit ...
sleep 5

# send messages to the monitor
./send-test-metrics.sh

# wait for the messages go to the database
echo waiting a bit longer ...
sleep 5

# check if the messages went to the database
./count-metrics.sh
TEST_RESULT=$?

# shutdown and tidy up
./shutdown-test.sh

exit $TEST_RESULT
