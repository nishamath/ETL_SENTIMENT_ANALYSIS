import boto3
from confluent_kafka import Consumer, KafkaError
import json
from datetime import datetime

# AWS S3 Configuration (credentials handled securely by environment or IAM role)
s3_client = boto3.client('s3', region_name='ap-south-1')  # Set your AWS region

# S3 bucket details
bucket_name = 'my-aws-task--new'  # Your S3 bucket name
file_name = 'consumed_messages/consumed_data.json'  # Path to the file where data will be stored

# Function to upload data to S3
def upload_to_s3(data):
    try:
        # Upload data to S3
        s3_client.put_object(Body=json.dumps(data), Bucket=bucket_name, Key=file_name)
        print(f"Successfully uploaded to S3: {file_name}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

# Function to consume messages and send to S3
def consume_messages_and_upload_to_s3(topic):
    consumer = Consumer({
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'news_group',
        'auto.offset.reset': 'earliest',
    })

    consumer.subscribe([topic])

    seen_messages = set()  # Set to track seen messages
    consumed_data = []  # List to accumulate consumed messages
    batch_size = 10  # Upload in batches of 10 messages, adjust as needed

    try:
        while True:
            msg = consumer.poll(1.0)  # Poll for messages with a 1-second timeout
            if msg is None:
                continue
            if msg.error() and msg.error().code() != KafkaError._PARTITION_EOF:
                print(f"Error: {msg.error()}")
                continue

            key = msg.key().decode('utf-8') if msg.key() else "No Key"
            value = msg.value().decode('utf-8') if msg.value() else "No Value"

            # Combine key and value for uniqueness (you can use just the value as well)
            message_id = (key, value)

            # Skip duplicate messages (based on key-value pair)
            if message_id in seen_messages:
                continue
            seen_messages.add(message_id)

            # Append the consumed message to the list
            consumed_data.append({
                'timestamp': datetime.utcnow().isoformat(),
                'key': key,
                'value': value
            })

            # Upload in batches
            if len(consumed_data) >= batch_size:
                upload_to_s3(consumed_data)  # Upload to S3
                consumed_data.clear()  # Clear the list after uploading

            # Print the consumed message to the console (optional)
            print(f"Consumed message:  - {value}")
            print('-' * 5)

    except KeyboardInterrupt:
        print("Consumption stopped.")
    finally:
        consumer.close()

if __name__ == "__main__":
    # Provide the topic to consume from
    consume_messages_and_upload_to_s3('news_topic1')
