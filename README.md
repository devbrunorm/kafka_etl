# Debezium/Spark ETL [WIP]

## Goals
- Learn more about Kafka Connect and Debezium
- Pratice with Spark Streaming

## Setup

### Requirements
- Docker
- Python

### Creating CDC with Debezium

Initialize Zookeeper:
```
sh ./scripts/zookeeper.sh
```

Initialize Kafka:
```
sh ./scripts/kafka.sh
```

Initialize Kafka UI:
```
sh ./scripts/kafka_ui.sh
```

Initialize example MySQL:
```
sh ./scripts/mysql.sh
```

Initialize Kafka Connect:
```
sh ./scripts/connect.sh
```

Kafka Debezium MySQL Connector to be added:
```
{
  "name": "inventory-connector",  
  "config": {  
    "connector.class": "io.debezium.connector.mysql.MySqlConnector",
    "tasks.max": "1",  
    "database.hostname": "mysql",  
    "database.port": "3306",
    "database.user": "debezium",
    "database.password": "dbz",
    "database.server.id": "184054",  
    "topic.prefix": "dbserver1",  
    "database.include.list": "inventory",  
    "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",  
    "schema.history.internal.kafka.topic": "schema-changes.inventory"  
  }
}
```

Add Connector:
```
sh ./scripts/create_connection.sh
```

### Read Streaming
Install pyspark
```
pip install -r requirements.txt
```

Run script:
```
python main.py
```