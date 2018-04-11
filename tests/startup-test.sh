#!/bin/bash
echo Starting components ...
docker-compose up -d
echo Done

echo Starting monitor ...
./run-monitor.sh
echo Done
