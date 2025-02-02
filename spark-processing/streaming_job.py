from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window, sum as _sum
from pyspark.sql.types import StructType, StringType, DoubleType, TimestampType
import redis
import json
KAFKA_SERVER = "54.89.218.218"
KAFKA_PORT = "9092"
REDIS_HOST = "3.86.145.243"
REDIS_PORT = "6379"
REDIS_PASS = "Test@1234"
TOPIC = "user_activity"


class ProcessStream():
    def __init__(self, spark, redis_client, topic):
        # Define schema for incoming data
        self.schema = StructType() \
                    .add("event_type", StringType()) \
                    .add("user_id", StringType()) \
                    .add("product_id", StringType()) \
                    .add("price", DoubleType()) \
                    .add("timestamp", TimestampType())
        self.spark = spark
        self.redis_client = redis_client
        self.topic = topic
    
    def __send_to_redis(self, df, epoch_id):
        partition = df.collect()
        for row in partition:
            key = f"product:{row['product_id']}"
            data = {
                "timestamp": row["window_end"].isoformat(),
                "price": round(row["total_revenue"], 2)  # Rounding for better readability
            }
            
            # Store multiple timestamped records in a List
            redis_client.lpush(key, json.dumps(data))
    
            # Keep only the last 100 records per product (FIFO strategy)
            redis_client.ltrim(key, 0, 99)

    # Read data from Kafka
    def __read_stream(self):
        return spark \
                .readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", f"{KAFKA_SERVER}:{KAFKA_PORT}") \
                .option("subscribe", self.topic) \
                .option("startingOffsets", "latest") \
                .load()
    
    def __tranform_data(self):
        # Parse the data
        df = self.__read_stream()
        parsed = df.selectExpr("CAST(value AS STRING)").select(from_json(col("value"), self.schema).alias("data")).select("data.*").where("event_type='purchase'")

        # Add watermark and aggregate data
        aggregated = parsed.withWatermark("timestamp", "10 minutes").groupBy(
                "product_id",
                window("timestamp", "5 minutes")  
            ) \
            .agg(_sum("price").alias("total_revenue")) \
            .select(
                col("product_id"),
                col("window.end").alias("window_end"),
                col("total_revenue")
        )
        return aggregated
    def write_to_sink(self):
        aggregated = self.__tranform_data()
        # Write aggregated data to Redis
        query = aggregated.writeStream \
            .foreachBatch(self.__send_to_redis) \
            .option("checkpointLocation", "D:\\temp\\") \
            .outputMode("update") \
            .start()

        query.awaitTermination()

if __name__ == "___main":
    # Initialize Redis connection
    redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASS, decode_responses=True)
    spark = SparkSession.builder.config("spark.jars.packages","org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1").master("local").appName("RealTime-ecommerce-data-processing").getOrCreate()

    process_stream = ProcessStream(spark, redis_client, TOPIC)
    process_stream.write_to_sink()