import json
from newsapi import NewsApiClient
from kafka import KafkaProducer
import csv

# Get your API key from https://newsapi.org/
key = "6003ec3c80f54c59ba534ae8ee0482a5"

# Initialize API endpoint
newsapi = NewsApiClient(api_key=key)

# Kafka producer configuration
topic = "my-news"

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers='localhost:9092')

# Define the list of media sources
sources = 'bbc-news,cnn,fox-news,nbc-news,the-guardian-uk,the-new-york-times,the-washington-post,usa-today,independent,daily-mail'

# Fetch articles from sources
all_articles = newsapi.get_everything(sources=sources, language='en')

# Send articles to Kafka topic
for article in all_articles['articles']:
    article['location'] = 'Paris, France'  # Adding a demo location
    producer.send(topic, json.dumps(article).encode('utf-8'))

# Close the Kafka producer
producer.close()

# Specify the filename for the CSV file
csv_filename = "news_articles.csv"

# Extract article data from JSON and save to CSV
try:
    # Open the CSV file for writing
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['title', 'description', 'url', 'publishedAt']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()

        # Iterate over the articles and write them to the CSV file
        for article in all_articles['articles']:
            writer.writerow({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'publishedAt': article['publishedAt']
            })

    print(f"Article data has been saved to {csv_filename}")
except Exception as e:
    print("An error occurred:", e)
