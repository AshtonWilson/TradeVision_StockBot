import requests
import getWeekday
from datetime import datetime
from dotenv import load_dotenv
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import portfolio_handler


def configure():
    """Load API keys from .env file"""
    load_dotenv()


# Load the portfolio and balance
balance, portfolio = portfolio_handler.read_portfolio('portfolio')

configure()

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

analyzer = SentimentIntensityAnalyzer()
overall_sentiment = {}
overall_performance = {}

# Fetch stock data and news for each stock in the portfolio
for stock in portfolio:
    # Get stock prices
    dict_alphavantage = {
        "function": "TIME_SERIES_DAILY",
        "symbol": stock,
        "apikey": os.getenv('api_key_alphavantage')
    }
    stock_response = requests.get(STOCK_ENDPOINT, dict_alphavantage)
    stock_response.raise_for_status()
    stock_dict = stock_response.json()

    # Get news
    dict_newsapi = {
        'q': stock,
        'language': 'en',
        'apiKey': os.getenv('api_key_newsapi')
    }
    news_response = requests.get(NEWS_ENDPOINT, dict_newsapi)
    news_response.raise_for_status()
    news_dict = news_response.json()

    # Calculate percent difference in stock price over the last two days
    today = datetime.today()
    previous_weekday = getWeekday.prev_weekday(today).strftime('%Y-%m-%d')
    day_before_previous_weekday = getWeekday.prev_weekday(getWeekday.prev_weekday(today)).strftime('%Y-%m-%d')

    try:
        yesterday_price = float(stock_dict["Time Series (Daily)"][previous_weekday]["4. close"])
        day_before_yesterday_price = float(stock_dict["Time Series (Daily)"][day_before_previous_weekday]["4. close"])
        price_diff = abs(yesterday_price - day_before_yesterday_price)
        percent_diff = (price_diff / yesterday_price) * 100
    except KeyError:
        print(f"Stock data not available for {stock}. Skipping...")
        continue

    # Perform sentiment analysis on news articles
    sentiment_scores = []
    for article in news_dict['articles']:
        text = f"{article['title']} {article['description']}"
        sentiment = analyzer.polarity_scores(text)
        sentiment_scores.append(sentiment['compound'])

    # Average sentiment score for this stock
    if sentiment_scores:
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
    else:
        avg_sentiment = 0

    # Store sentiment and performance for each stock
    overall_sentiment[stock] = avg_sentiment
    overall_performance[stock] = percent_diff

# Decision-making based on overall portfolio sentiment and performance
for stock in portfolio:
    avg_sentiment = overall_sentiment[stock]
    percent_diff = overall_performance[stock]

    print(f"Stock: {stock}, Sentiment: {avg_sentiment:.2f}, Price Change: {percent_diff:.2f}%")
# Todo fix logic so that it does not spend all the money on the first stock it wants to buy
    if avg_sentiment > 0.5 and percent_diff > 2:
        decision = "BUY"
        quantity_to_buy = int(balance // yesterday_price)
        portfolio[stock] += quantity_to_buy
        balance -= quantity_to_buy * yesterday_price
    elif avg_sentiment < -0.2 and percent_diff < -2 and portfolio[stock] > 0:
        decision = "SELL"
        balance += portfolio[stock] * yesterday_price
        portfolio[stock] = 0
    else:
        decision = "HOLD"

    # Output decision for each stock
    print(f"{stock}: Decision: {decision}, Updated Stock: {portfolio[stock]}, Updated Balance: ${balance:.2f}")

# Update the portfolio file after making decisions
portfolio_handler.write_portfolio('portfolio', balance, portfolio)
