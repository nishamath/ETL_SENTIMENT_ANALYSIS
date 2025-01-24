from pyspark.sql import SparkSession
from pyspark.sql.functions import col, json_tuple, coalesce, lit

spark = SparkSession.builder \
    .appName("YourAppName") \
    .config("spark.jars", "/home/nisha/hadoop/spark1/spark-3.5.1-bin-hadoop3/jars/postgresql-42.2.23.jar") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()

# Kafka parameters
kafka_broker = 'localhost:9092'
topic_name = 'news_topic1'

# PostgreSQL connection properties
db_properties = {
    "user": "postgres",
    "password": "123456",
    "driver": "org.postgresql.Driver"
}
db_url = "jdbc:postgresql://localhost:5432/my_new"

# Checkpoint directory for tracking stream progress
checkpoint_dir = "/tmp/kafka_checkpoint"

# Read stream from Kafka
kafkaStreamDF = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topic_name) \
    .option("startingOffsets", "earliest") \
    .option("failOnDataLoss", "false") \
    .load()

# Select the value column and cast it to string
articlesDF = kafkaStreamDF.selectExpr("CAST(value AS STRING) as json")

# Parse JSON and select fields (Ensure the JSON data has "title", "source", and "description")
processedDF = articlesDF.select(
    json_tuple(col("json"), "title", "source", "description").alias("title", "source", "description")
)

# Debugging: Print out a few rows for verification
processedDF.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Define a function to write each micro-batch to PostgreSQL
def write_to_postgresql(df, epoch_id):
    try:
        if df.isEmpty():
            print(f"Micro-batch {epoch_id} has no data to write.")
            return

        # Print schema and sample data for debugging
        print(f"Schema for micro-batch {epoch_id}:")
        df.printSchema()
        print(f"Sample data from micro-batch {epoch_id}:")
        df.show(5)

        # Replace null description with a default value
        df = df.withColumn("description", coalesce(col("description"), lit("No description available")))

        # Cast columns explicitly to string to match PostgreSQL schema
        df = df.select(
            col("title").cast("string"),
            col("source").cast("string"),
            col("description").cast("string")
        )

        # Filter out rows with null values in critical columns
        df = df.filter(col("title").isNotNull() & col("source").isNotNull())

        # Write the processed DataFrame to PostgreSQL table
        if df.count() > 0:
            df.write \
                .jdbc(url=db_url, table="streaming_data2", mode="append", properties=db_properties)
            print(f"Micro-batch {epoch_id} written to PostgreSQL successfully!")
        else:
            print(f"Micro-batch {epoch_id} has no valid data to write.")

    except Exception as e:
        print(f"Error writing micro-batch {epoch_id} to PostgreSQL: {e}")

# Write stream to PostgreSQL
query = processedDF.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_postgresql) \
    .option("checkpointLocation", checkpoint_dir) \
    .start()

# Wait for the computation to terminate
query.awaitTermination()
