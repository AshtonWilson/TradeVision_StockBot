import requests
import getWeekday
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

def configure():
    """Used to load api keys, if you fork this project add your own api keys for the endpoints mentioned below"""
    load_dotenv()


configure()
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

dict_alphavantage = {"function": "TIME_SERIES_DAILY",
                     "symbol": STOCK_NAME,
                     "apikey": os.getenv('api_key_alphavantage')}

dict_newsapi = {'q': STOCK_NAME,
                'language': 'en',
                'apiKey': os.getenv('api_key_newsapi')}

response = requests.get(STOCK_ENDPOINT, dict_alphavantage)
response.raise_for_status()
stock_dict = response.json()

news_response = requests.get(NEWS_ENDPOINT, dict_newsapi)
news_response.raise_for_status()
news_dict = news_response.json()

# Get dates
today = datetime.today()
previous_weekday = getWeekday.prev_weekday(today)
day_before_previous_weekday = getWeekday.prev_weekday(previous_weekday)
# correct date formatting
previous_weekday = previous_weekday.strftime('%Y-%m-%d')
day_before_previous_weekday = day_before_previous_weekday.strftime('%Y-%m-%d')

yesterday_price = (stock_dict["Time Series (Daily)"][previous_weekday]["4. close"])
day_before_yesterday_price = (stock_dict["Time Series (Daily)"][day_before_previous_weekday]["4. close"])
positive_diff = abs(float(yesterday_price) - float(day_before_yesterday_price))
percent_diff = (positive_diff / float(yesterday_price)) * 100

# Sentiment analysis
analyzer = SentimentIntensityAnalyzer()
sentiment_scores = []

# Extract news headlines and descriptions for sentiment analysis
for article in news_dict['articles']:
    text = f"{article['title']} {article['description']}"
    sentiment = analyzer.polarity_scores(text)
    sentiment_scores.append(sentiment['compound'])

# Calculate the average sentiment score
avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)

# Trading decision logic
starting_balance = 20000  # Initial balance
stock_inventory = 0     # Number of stocks owned (if any)

if avg_sentiment > 0.4 and percent_diff > 2:
    decision = "BUY"
    quantity_to_buy = starting_balance // yesterday_price
    stock_inventory += quantity_to_buy
    starting_balance -= quantity_to_buy * yesterday_price
elif avg_sentiment < -0.5 and percent_diff < -2:
    decision = "SELL"
    starting_balance += stock_inventory * yesterday_price
    stock_inventory = 0
else:
    decision = "HOLD"

# Print the decision and the updated balance
print(f"Decision: {decision}")
print(f"Stock Inventory: {stock_inventory}")
print(f"Balance: ${starting_balance:.2f}")