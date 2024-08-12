import os
from kafka import KafkaConsumer
import json
import csv

# Kafka consumer configuration
topic = "my-news"  # Replace with your Kafka topic name
brokers = "localhost:9092"  # Replace with your Kafka broker(s)

# Create the Kafka consumer
consumer = KafkaConsumer(topic,
                         bootstrap_servers=brokers,
                         auto_offset_reset='earliest',
                         enable_auto_commit=False,
                         group_id='my-consumer-group')  # Replace with your consumer group ID

# Create an empty list to store the article data
article_data = []

# Consume messages
for message in consumer:
    article = json.loads(message.value.decode('utf-8'))
    article_data.append(article)

    # Print the fetched data
    print("Title:", article['title'])
    print("Description:", article['description'])
    print("URL:", article['url'])
    print("Published At:", article['publishedAt'])
    print("Location:", article.get('location', ''))
    print("-" * 50)

# Specify the pathname for the CSV file
csv_pathname = "/home/anu_siwach28/news_articles.csv"

try:
    # Write the article data to the CSV file
    with open(csv_pathname, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['title', 'description', 'url', 'publishedAt', 'location']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for article in article_data:
            writer.writerow({
                'title': article['title'],
                'description': article['description'],
                'url': article['url'],
                'publishedAt': article['publishedAt'],
                'location': article.get('location', '')  # Location might not always be present
            })

    print(f"Article data has been saved to {csv_pathname}")
except Exception as e:
    print("An error occurred:", e)

