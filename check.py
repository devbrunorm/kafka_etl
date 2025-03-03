from pyspark.sql import SparkSession
from pyspark.sql import functions as f

scala_version = '2.12'
spark_version = '3.5.3'
delta_version = '3.3.0'
packages = [
    f'org.apache.spark:spark-sql-kafka-0-10_{scala_version}:{spark_version}',
    'org.apache.kafka:kafka-clients:3.2.0',
    f'io.delta:delta-spark_{scala_version}:{delta_version}'
]

spark = SparkSession\
    .builder\
    .appName("KafkaSparkStreaming")\
    .master("local[*]") \
    .config('spark.jars.packages', ','.join(packages))\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
    .getOrCreate()

df = spark.read.format("delta").load("delta/customers")
df.show()
print(df.count())

df.select(f.min("id"), f.max("id")).show()