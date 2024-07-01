import os
import requests
from datetime import date, timedelta

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCKS_API_KEY = os.environ.get("STOCKS_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")


def get_stock_difference_perc(stock:str) -> float:
    """
    Calculates the difference between the last and second last entry of a stock in percentage
    :param stock: stock name. egs: IBM, TSLA etc
    :return: the percentage increase or decrease between the last and second last entry of a stock
    """

    # Get the last 100 entries on stock information
    url = "https://www.alphavantage.co/query"

    params = \
        {
            "function": "TIME_SERIES_DAILY",
            "symbol": stock,
            "apikey": STOCKS_API_KEY,
        }

    response = requests.get(url=url, params=params)
    response.raise_for_status()
    json = response.json()

    # stocks are not recorded on weekends. Accommodate for that.
    if date.today().day == 1:
        days_since_last_entry = 3
        days_since_second_last_entry = 4
    elif date.today().day == 2:
        days_since_last_entry = 1
        days_since_second_last_entry = 4
    else:
        days_since_last_entry = 1
        days_since_second_last_entry = 2

    # get the dates of the last 2 recorded stocks in the correct format
    last_entry = (date.today() - timedelta(days=days_since_last_entry)).strftime("%Y-%m-%d")
    second_last_entry = (date.today() - timedelta(days=days_since_second_last_entry)).strftime("%Y-%m-%d")

    # get the last 2 entries, at close time
    last_stock_price = float(json["Time Series (Daily)"][last_entry]["4. close"])
    second_last_stock_price = float(json["Time Series (Daily)"][second_last_entry]["4. close"])

    # calculate the percentage difference
    stock_difference = last_stock_price - second_last_stock_price
    return (stock_difference / second_last_stock_price) * 100


## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
def get_news(query):
    url = "https://newsapi.org/v2/everything"

    if date.today().day == 1:
        from_date = (date.today() - timedelta(days=4)).strftime("%Y-%m-%d")
    elif date.today().day == 2:
        from_date = (date.today() - timedelta(days=4)).strftime("%Y-%m-%d")
    else:
        from_date = (date.today() - timedelta(days=2)).strftime("%Y-%m-%d")

    params = \
        {
            "q":query,
            "apikey": NEWS_API_KEY,
            "from": from_date,
        }

    response = requests.get(url=url, params=params)
    response.raise_for_status()
    print(response.json())


## STEP 3: Use https://www.twilio.com
# Send a separate message with the percentage change and each article's title and description to your phone number.


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
#
# stock_difference_perc = get_stock_difference_perc(STOCK)
# if -5 <= stock_difference_perc >= 5:
#     get_news(COMPANY_NAME)
# else:
#     print(stock_difference_perc)

get_news(COMPANY_NAME)