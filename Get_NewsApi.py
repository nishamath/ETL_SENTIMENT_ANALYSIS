import requests
# Function to return configurations
def get_config():
    return {
        "base_url": "https://newsapi.org/v2/top-headlines",
        "country": "us",
        "category": "business",
        "api_key": "82868f075bc9496f9f6410171fb45fe1",  # Replace with your valid API key
        "kafka_broker": "localhost:9092",  # Replace with your Kafka broker if needed
        "topic": "news_topic1",  # Replace with your Kafka topic if needed
    }


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


# Main script
def main():
    articles = fetch_articles()  # Fetch articles

    if articles:
        # Print each article's details
        for idx, article in enumerate(articles, start=1):
            title = article.get('title', 'No Title')  # Use 'No Title' if missing
            source = article.get('source', {}).get('name', 'Unknown Source')  # Handle nested key
            description = article.get('description', 'No Description Available')  # Fallback description

            print(f"Article {idx}")
            print(f"Title: {title}")
            print(f"Source: {source}")
            print(f"Description: {description}")
            print("-" * 40)  # Separator
    else:
        print("No articles found or 'articles' key is missing.")


if __name__ == "__main__":
    main()

