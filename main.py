from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, expr, from_json, col

scala_version = '2.12'
spark_version = '3.5.4'
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.0'
]

def persist_data(batch_df, batch_id):
    batch_df.persist()
    json_schema = spark.read.json(batch_df.select(col("value").alias("j")).rdd.map(lambda x: x.j)).schema
    batch_df = batch_df.withColumn("values_json", from_json(col("value"), json_schema))
    batch_df.show()
    # batch_df = batch_df.select("values_json.payload.after.*")
    # batch_df.printSchema()
    batch_df.unpersist()

spark = SparkSession\
    .builder\
    .appName("KafkaSparkStreaming")\
    .master("local[*]") \
    .config('spark.jars.packages', ','.join(packages))\
    .getOrCreate()

# df = spark \
#     .read \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "localhost:9092") \
#     .option("stratingOffsets", "earliest") \
#     .option("subscribe", "customers-connector-v1.customers.customers") \
#     .load()

# df = df.withColumn("value", expr("cast(value as string)"))
# json_schema = spark.read.json(df.select(col("value").alias("j")).rdd.map(lambda x: x.j)).schema
# df = df.withColumn("values_json", from_json(col("value"), json_schema))
# df = df.select("values_json.payload.after.*")
# df.show()

streaming = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("stratingOffsets", "earliest") \
    .option("subscribe", "customers-connector-v1.customers.customers") \
    .load()

streaming.selectExpr("cast(value as string) as value")\
            .writeStream\
            .foreachBatch(persist_data)\
            .outputMode("append")\
            .start().awaitTermination()

# streaming = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
#     .writeStream \
#     .format("console") \
#     .outputMode("append") \
#     .start().awaitTermination()

    # .trigger(availableNow=True) \
    # .option("checkpointLocation", "checkpoint") \
    # .option("path", "output")\