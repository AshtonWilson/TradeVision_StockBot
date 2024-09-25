import requests
import getWeekday
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import portfolio_handler

def configure():
    """Used to load api keys, if you fork this project add your own api keys for the endpoints mentioned below"""
    load_dotenv()

balance, portfolio = portfolio_handler.read_portfolio('portfolio')

print(portfolio.keys())

configure()

COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

for key in portfolio.keys():
    dict_alphavantage = {"function": "TIME_SERIES_DAILY",
                         "symbol": key,
                         "apikey": os.getenv('api_key_alphavantage')}
    stock_response = requests.get(STOCK_ENDPOINT, dict_alphavantage)
    stock_response.raise_for_status()
    stock_dict = stock_response.json()
    print(stock_dict)
for name in portfolio.keys():

    dict_newsapi = {'q': name,
                    'language': 'en',
                    'apiKey': os.getenv('api_key_newsapi')}

    news_response = requests.get(NEWS_ENDPOINT, dict_newsapi)
    news_response.raise_for_status()
    news_dict = news_response.json()
    print(news_dict)
# Todo add the get dates block to the above loop to get prices for each stock in the portfolio
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
# Todo incorporate sentiment analysis into a loop so it runs for each stock
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
stock_inventory = 0     # Number of stocks owned (if any)

if avg_sentiment > 0.5 and percent_diff > 2:
    decision = "BUY"
    quantity_to_buy = balance // yesterday_price
    stock_inventory += quantity_to_buy
    balance -= quantity_to_buy * yesterday_price
elif avg_sentiment < -0.5 and percent_diff < -2:
    decision = "SELL"
    balance += stock_inventory * yesterday_price
    stock_inventory = 0
else:
    decision = "HOLD"

# Print the decision and the updated balance
print(f"Decision: {decision}")
print(f"Stock Inventory: {stock_inventory}")
print(f"Balance: ${balance:.2f}")