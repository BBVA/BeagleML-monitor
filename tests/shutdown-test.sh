#!/bin/bash
echo Stopoing monitor ...
docker stop tests_monitor
docker rm tests_monitor

echo Stopping components
docker-compose down
