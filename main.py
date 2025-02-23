from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split, expr

scala_version = '2.12'
spark_version = '3.5.4'
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.0'
]

spark = SparkSession\
    .builder\
    .appName("StructuredNetworkWordCount")\
    .config('spark.jars.packages', ','.join(packages))\
    .getOrCreate()

df = spark \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("stratingOffsets", "earliest") \
    .option("subscribe", "dbserver1.inventory.customers") \
    .load()

print(df.select("value")
  .writeStream
  .format("console")
  .foreachBatch(print)
  .start())

# (df.select("topic", "value")
#     .writeStream
#     .format("console")
#     # .option("checkpointLocation", self.configs['checkpoint_location'])
#     # .foreachBatch(persist_data)
#     .outputMode("append")
#     .option("path", "output")
#     .start().awaitTermination())

# df.select("value").show()