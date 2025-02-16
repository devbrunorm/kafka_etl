#!/bin/bash

CONTAINER_NAME="kafka-ui"

# Check if container is already running
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
    echo "O container $CONTAINER_NAME já está em execução."
    exit 1
fi

docker run -it --rm \
    --name kafka-ui \
    -p 8080:8080 \
    --link kafka:kafka \
    -e KAFKA_CLUSTERS_0_NAME=local \
    -e KAFKA_CLUSTERS_0_BOOTSTRAPSERVERS=kafka:9092 \
    -e KAFKA_CLUSTERS_0_ZOOKEEPER=zookeeper:2181 \
    provectuslabs/kafka-ui