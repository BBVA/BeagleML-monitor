#!/bin/bash

EXPECTED='"count" : 3'
RESP=$(./run-query.sh countMetrics.qry)

if echo "$RESP" | grep -q "$EXPECTED"; then
    echo count-metrics test: OK
    exit 0;
else
    echo count-metrics test: FAIL
    echo $RESP
    exit 1;
fi
