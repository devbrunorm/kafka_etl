#!/bin/bash

CONTAINER_NAME="kafka"

# Check if container is already running
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
    echo "O container $CONTAINER_NAME já está em execução."
    exit 1
fi

docker run -it --rm \
    --name kafka \
    -p 9092:9092 \
    --link zookeeper:zookeeper \
    quay.io/debezium/kafka:3.0