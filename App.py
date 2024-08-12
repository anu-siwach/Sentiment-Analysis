import streamlit as st
import json
from textblob import TextBlob
from newsapi import NewsApiClient

# Initialize the News API client
key = "6003ec3c80f54c59ba534ae8ee0482a5"
newsapi = NewsApiClient(api_key=key)

st.title("News Sentiment Analysis")

# Create a button to fetch news articles
if st.button("Fetch News Articles"):
    # Fetch articles from the News API
    articles = newsapi.get_everything(q='technology', language='en')

    for article in articles['articles']:
        st.write("Title:", article['title'])
        st.write("Description:", article['description'])
        st.write("URL:", article['url'])

        # Perform sentiment analysis
        blob = TextBlob(article['description'])
        sentiment = blob.sentiment

        st.write("Sentiment Polarity:", sentiment.polarity)
        st.write("Sentiment Subjectivity:", sentiment.subjectivity)

