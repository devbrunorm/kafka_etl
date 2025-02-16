#!/bin/bash

CONTAINER_NAME="connect"

# Check if container is already running
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
    echo "O container $CONTAINER_NAME já está em execução."
    exit 1
fi

docker run -it --rm \
    --name connect \
    -p 8083:8083 \
    -e GROUP_ID=1 \
    -e CONFIG_STORAGE_TOPIC=my_connect_configs \
    -e OFFSET_STORAGE_TOPIC=my_connect_offsets \
    -e STATUS_STORAGE_TOPIC=my_connect_statuses \
    --link kafka:kafka \
    --link mysql:mysql \
    quay.io/debezium/connect:3.0