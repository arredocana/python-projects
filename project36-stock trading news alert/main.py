import os
import pandas as pd
from newsapi import NewsApiClient
# import requests
from twilio.rest import Client
from dotenv import load_dotenv
import logging
from config import create_twitter_api

# APIs
load_dotenv('.env')
NEWS_API = os.getenv("NEWS_API_KEY")
ALPHAV_API = os.getenv("ALPHAV_API_KEY")

TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

# ENDPOINTS
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
CHANGE = 1
PHONE_NUMBER = os.getenv("PHONE_NUMBER")

stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHAV_API,
    "datatype": "csv"
}

# Optionally
# data = requests.get(STOCK_ENDPOINT, stock_params).text

# stock_data = pd.DataFrame(
#     [x.split(',') for x in data.split('\r\n')[1:]],
#     columns=[x for x in data.split('\r\n')[0].split(',')]
# )

stock_url = f"{STOCK_ENDPOINT}?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={ALPHAV_API}&datatype=csv"
up_down = None

# create logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def check_closing_price(stock_data):
    yesterday_closing_price = stock_data['close'][0]
    day_before_yesterday_closing_price = stock_data['close'][1]

    difference = (yesterday_closing_price-day_before_yesterday_closing_price)/yesterday_closing_price

    global up_down
    if difference > 0:
        up_down = '🔺'
    else:
        up_down = '🔻'

    diff_percent = round(abs(difference)*100, 2)

    return diff_percent


def get_news(api, from_date, to_date):

    newsapi = NewsApiClient(api_key=api)
    logger.info("Getting latest news...")

    all_articles = newsapi.get_everything(
        q=COMPANY_NAME,
        from_param=from_date,
        to=to_date,
        language='en'
    )

    return all_articles["articles"]


def send_sms(messages):

    twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    for message in messages:
        message = twilio.messages.create(
            body=message,
            from_='+16092566459',
            to=PHONE_NUMBER
        )

        logger.info(message.status)


def send_tweet(messages):

    twitter = create_twitter_api()

    original_tweet = twitter.update_status(status=messages[0]+' 👇')

    reply_tweet_id = original_tweet.id

    for message in messages[1:]:
        if len(message) > 150:
            message = message[:147]+'...'

        reply_tweet = twitter.update_status(
            status=message,
            in_reply_to_status_id=reply_tweet_id,
            auto_populate_reply_metadata=True
        )
        reply_tweet_id = reply_tweet.id

    logger.info('tweets sent!')


def main():

    data = pd.read_csv(stock_url)
    from_date = data['timestamp'][1]
    to_date = data['timestamp'][1]

    diff_percent = check_closing_price(data)

    if diff_percent > CHANGE:

        # Get latest news
        news = get_news(NEWS_API, from_date, to_date)

        top_3_articles = news[:3]

        # Send SMS with Twilio

        # formatted_articles = [
        #     f"{STOCK}: {up_down} {diff_percent}%\
        #     \nHeadline: {article['title']}.\
        #     \nBrief: {article['description']}" for article in top_3_articles
        # ]

        # send_sms(messages=formatted_articles)

        tweets = [f"{STOCK}: {up_down} {diff_percent}%"]

        for article in top_3_articles:
            tweets.append(f"{article['title']}:\n{article['description']}")

        # formatted_new = f"{STOCK}: {up_down}{diff_percent}% {new['title']}"

        send_tweet(tweets)


if __name__ == "__main__":
    main()
