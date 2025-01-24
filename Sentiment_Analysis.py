from pyspark.sql import SparkSession
from pyspark.sql.functions import col, json_tuple, coalesce, lit, udf
from pyspark.sql.types import FloatType
from textblob import TextBlob

# Initialize Spark session
spark = SparkSession.builder \
    .appName("SentimentAnalysis") \
    .config("spark.jars", "/home/nisha/hadoop/spark1/spark-3.5.1-bin-hadoop3/jars/postgresql-42.2.23.jar") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1") \
    .getOrCreate()

# Kafka and PostgreSQL parameters
kafka_broker = 'localhost:9092'
topic_name = 'news_topic1'
db_url = "jdbc:postgresql://localhost:5432/my_new"
db_properties = {
    "user": "postgres",
    "password": "123456",
    "driver": "org.postgresql.Driver"
}


# Sentiment analysis function using TextBlob
def get_sentiment(text):
    if text:
        sentiment = TextBlob(text).sentiment.polarity
        if sentiment == 0:  # Neutral sentiment case
            return 0.0
        return sentiment
    return 0.0


# Register UDF for sentiment analysis
sentiment_udf = udf(get_sentiment, FloatType())

# Read stream from Kafka
kafkaStreamDF = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", kafka_broker) \
    .option("subscribe", topic_name) \
    .option("startingOffsets", "earliest") \
    .load()

# Parse JSON and select fields (title, source, description)
articlesDF = kafkaStreamDF.selectExpr("CAST(value AS STRING) as json")

# Extract relevant fields
processedDF = articlesDF.select(
    json_tuple(col("json"), "title", "source", "description").alias("title", "source", "description")
)

# Perform sentiment analysis on the description
processedDF = processedDF.withColumn("sentiment_score", sentiment_udf(col("description")))

# Clean and filter data
processedDF = processedDF.withColumn("description", coalesce(col("description"), lit("No description available")))
processedDF = processedDF.select(
    col("title").cast("string"),
    col("source").cast("string"),
    col("description").cast("string"),
    col("sentiment_score").cast("float")
)
processedDF = processedDF.filter(col("title").isNotNull() & col("source").isNotNull())

# Debugging: write data to the console for inspection
debug_query = processedDF.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", "false") \
    .start()

# Wait for the query to finish
debug_query.awaitTermination()


# Write stream to PostgreSQL with a limit of 20 rows per batch
def write_to_postgresql(df, epoch_id):
    try:
        if df.isEmpty():
            print(f"Micro-batch {epoch_id} has no data to write.")
            return

        # Limit to 20 rows per batch
        df = df.limit(20)

        # Write to PostgreSQL
        df.write \
            .jdbc(url=db_url, table="streaming_data2", mode="append", properties=db_properties)
        print(f"Micro-batch {epoch_id} written to PostgreSQL successfully!")

    except Exception as e:
        print(f"Error writing micro-batch {epoch_id} to PostgreSQL: {e}")


# Start the main stream and process data
main_query = processedDF.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_postgresql) \
    .option("checkpointLocation", "/tmp/kafka_checkpoint") \
    .start()

main_query.awaitTermination()
