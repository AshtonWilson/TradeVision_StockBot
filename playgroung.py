import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
from dotenv import load_dotenv
import os

def configure():
    """Load API keys"""
    load_dotenv()

configure()

# Configuration for APIs
STOCK_NAME = "TSLA"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# News API request
dict_newsapi = {
    'q': STOCK_NAME,
    'language': 'en',
    'apiKey': os.getenv('api_key_newsapi')
}

news_response = requests.get(NEWS_ENDPOINT, dict_newsapi)
news_response.raise_for_status()
news_dict = news_response.json()

# Sentiment Analyzers
vader_analyzer = SentimentIntensityAnalyzer()

# Storage for results
comparison_results = []

# Compare VADER and TextBlob
for article in news_dict['articles']:
    text = f"{article['title']} {article['description']}"

    # VADER sentiment analysis
    vader_sentiment = vader_analyzer.polarity_scores(text)['compound']

    # TextBlob sentiment analysis
    textblob_sentiment = TextBlob(text).sentiment.polarity

    comparison_results.append({
        'text': text,
        'vader_sentiment': vader_sentiment,
        'textblob_sentiment': textblob_sentiment
    })

# Display the comparison
for result in comparison_results:
    print(f"Text: {result['text'][:100]}...")  # Limiting to 100 chars for readability
    print(f"VADER Sentiment: {result['vader_sentiment']}")
    print(f"TextBlob Sentiment: {result['textblob_sentiment']}\n")
