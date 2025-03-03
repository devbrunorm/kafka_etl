from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, expr, from_json, col
from delta.tables import DeltaTable

scala_version = '2.12'
spark_version = '3.5.3'
delta_version = '3.3.0'
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.0',
    f'io.delta:delta-spark_{scala_version}:{delta_version}'
]

DELTA_LOCATION = "delta/customers"

def persist_data(batch_df, batch_id):
    batch_df.persist()
    print("--------------NOVO BATCH--------------")
    batch_df.show()
    json_schema = spark.read.json(batch_df.select(col("value").alias("j")).rdd.map(lambda x: x.j)).schema
    batch_df = batch_df.withColumn("values_json", from_json(col("value"), json_schema))
    batch_df.show()
    if batch_df.count() > 0:
        batch_df = batch_df.select("values_json.payload.after.*")
        batch_df.show()
        if not DeltaTable.isDeltaTable(spark, DELTA_LOCATION):
            batch_df.write.format("delta").mode("overwrite").save(DELTA_LOCATION)
        else:
            delta_table = DeltaTable.forPath(spark, DELTA_LOCATION)
            delta_table.alias("old").merge(batch_df.alias("new"), "old.id = new.id") \
                .whenMatchedUpdateAll() \
                .whenNotMatchedInsertAll() \
                .execute()
    
    batch_df.unpersist()

spark = SparkSession\
    .builder\
    .appName("KafkaSparkStreaming")\
    .master("local[*]") \
    .config('spark.jars.packages', ','.join(packages))\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
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