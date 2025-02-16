#!/bin/bash

CONTAINER_NAME="zookeeper"

# Check if container is already running
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
    echo "O container $CONTAINER_NAME já está em execução."
    exit 1
fi

docker run -it --rm \
    --name $CONTAINER_NAME \
    -p 2181:2181 \
    -p 2888:2888 \
    -p 3888:3888 \
    quay.io/debezium/zookeeper:3.0