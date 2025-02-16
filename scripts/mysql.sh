#!/bin/bash

CONTAINER_NAME="mysql"

# Check if container is already running
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
    echo "O container $CONTAINER_NAME já está em execução."
    exit 1
fi

docker run -it --rm \
    --name mysql \
    -p 3306:3306 \
    -e MYSQL_ROOT_PASSWORD=debezium \
    -e MYSQL_USER=mysqluser \
    -e MYSQL_PASSWORD=mysqlpw \
    quay.io/debezium/example-mysql:3.0