import os
import pandas as pd
from newsapi import NewsApiClient
import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
CHANGE = 10

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

NEWS_API = os.environ.get("NEWS_API_KEY")
ALPHAV_API = os.environ.get("ALPHAV_API_KEY")
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = os.environ["PHONE_NUMBER"]


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHAV_API,
    "datatype": "csv"
}

# response = requests.get(STOCK_ENDPOINT, params=stock_params)
# data = response.json()["Time Series (Daily)"]
# data_list = [value for (_, value) in data.items()]

# yesterday_data = data_list[0]
# yesterday_closing_price = float(yesterday_data["4. close"])

# day_before_yesterday_data = data_list[1]
# day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])


stock_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK}&apikey={ALPHAV_API}&datatype=csv"

stock_data = pd.read_csv(stock_url)

yesterday_closing_price = stock_data['close'][0]
day_before_yesterday_closing_price = stock_data['close'][1]

difference = (yesterday_closing_price-day_before_yesterday_closing_price)/yesterday_closing_price

up_down = None

if difference > 0:
    up_down = '🔺'
else:
    up_down = '🔻'

diff_percent = round(abs(difference)*100, 2)


def get_news(api):
    newsapi = NewsApiClient(api_key=api)

    all_articles = newsapi.get_everything(
        q=COMPANY_NAME,
        from_param=stock_data['timestamp'][1],
        to=stock_data['timestamp'][0],
        language='en'
    )

    top_3_articles = all_articles["articles"][:3]

    formatted_articles = [
        f"{STOCK}: {up_down} {diff_percent}%\
            \nHeadline: {article['title']}.\
            \nBrief: {article['description']}" for article in top_3_articles
    ]

    # news = {}

    # for index, article in enumerate(top_3_articles):
    #     news[f'top_{index+1}'] = {k:v for k, v in article.items() if k=='title' or k=='description'}

    return formatted_articles


if diff_percent > CHANGE:
    
    client = Client(account_sid, auth_token)

    top_news = get_news(NEWS_API)

    for new in top_news:
        # headline = top_news[new]["title"]
        # brief = top_news[new]["description"]

        message = client.messages.create(
            body=new,
            # body=f"{STOCK}: {up_down}{diff_percent}%\nHeaderline: {headline}\nBrief: {brief}",
            from_='+16092566459',
            to=PHONE_NUMBER
        )
        
        print(message.status)
