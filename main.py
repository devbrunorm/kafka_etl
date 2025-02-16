from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split

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
    .option("subscribe", "dbserver1.inventory.customers") \
    .load()

df.printSchema()