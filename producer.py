import requests
from kafka import KafkaProducer
import json
from Get_NewsApi import get_config  # Import the configuration function



# Fetch articles from the API
def fetch_articles():
    config = get_config()  # Get configuration
    url = f"{config['base_url']}?country={config['country']}&category={config['category']}&apiKey={config['api_key']}"

    # Send the GET request
    response = requests.get(url)

    # Check if the response is successful
    if response.status_code == 200:
        data = response.json()  # Parse the response JSON
        return data.get("articles", [])  # Return articles or an empty list
    else:
        print(f"Failed to fetch articles. HTTP Status: {response.status_code}")
        return []


# Send articles to Kafka
def send_to_kafka(articles):
    config = get_config()
    producer = KafkaProducer(
        bootstrap_servers=config["kafka_broker"],
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    print(f"Fetched {len(articles)} articles. Sending to Kafka...\n")

    for idx, article in enumerate(articles, start=1):
        title = article.get('title', 'No Title')  # Use 'No Title' if missing
        source = article.get('source', {}).get('name', 'Unknown Source')  # Handle nested key
        description = article.get('description', 'No description available')  # Fallback description

        # Construct the article data
        article_data = {
            "title": title,
            "source": source,
            "description": description
        }


        # Send the article to Kafka
        producer.send(config["topic"], value=article_data)


        # Print formatted article
        print(f"Article {idx}:")
        print(f"Title: {title}")
        print(f"Source: {source}")
        print(f"Description: {description}\n")


# Main script
def main():
    articles = fetch_articles()  # Fetch articles

    if articles:
        send_to_kafka(articles)  # Send articles to Kafka
    else:
        print("No articles found or 'articles' key is missing.")


if __name__ == "__main__":
    main()



