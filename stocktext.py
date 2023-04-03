import requests
from twilio.rest import Client

# Set up constants
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHAVANTAGE_API_KEY = "<insert_alphavantage_api_key_here>"
NEWS_API_KEY = "<insert_news_api_key_here>"
TWILIO_ACCOUNT_SID = "<insert_twilio_account_sid_here>"
TWILIO_AUTH_TOKEN = "<insert_twilio_auth_token_here>"
TWILIO_FROM_NUMBER = "<insert_twilio_from_number_here>"
TWILIO_TO_NUMBER = "<insert_twilio_to_number_here>"

# Set up endpoints
ALPHAVANTAGE_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": ALPHAVANTAGE_API_KEY,
}

response = requests.get(ALPHAVANTAGE_ENDPOINT, params=stock_params)
response.raise_for_status()

data = response.json()["Time Series (Daily)"]
yesterday_data = next(iter(data.values()))
yesterday_closing_price = float(yesterday_data["4. close"])
print(f"Yesterday's closing price: ${yesterday_closing_price:.2f}")

# Get the day before yesterday's closing stock price
day_before_yesterday_data = next(iter(data.values()), None)
if day_before_yesterday_data:
    day_before_yesterday_closing_price = float(day_before_yesterday_data["4. close"])
    print(f"Day before yesterday's closing price: ${day_before_yesterday_closing_price:.2f}")
    # Calculate the price difference and percentage difference
    price_difference = yesterday_closing_price - day_before_yesterday_closing_price
    price_difference_percentage = price_difference / day_before_yesterday_closing_price * 100
    price_difference_percentage_abs = abs(price_difference_percentage)
    if price_difference > 0:
        up_down = "🔺"
    else:
        up_down = "🔻"
    print(f"Price difference: {up_down}${price_difference:.2f} ({price_difference_percentage:+.2f}%)")
else:
    print("Unable to get day before yesterday's closing price.")

# Get news articles
news_params = {
    "qInTitle": COMPANY_NAME,
    "sortBy": "relevancy",
    "apiKey": NEWS_API_KEY,
}
news_response = requests.get(NEWS_ENDPOINT, params=news_params)
news_response.raise_for_status()
articles = news_response.json()["articles"][:3]
formatted_articles = [f"{article['title']}\n{article['description']}\n{article['url']}" for article in articles]

# Send SMS with news articles
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_=TWILIO_FROM_NUMBER,
        to=TWILIO_TO_NUMBER
    )
    print(f"Sent message: {message.sid}")


# code is a modified version of a script that uses an API to get the stock price and news articles related to a particular company, and sends an SMS message with the information. It can be used to keep track of stock prices and related news articles for a particular company, and receive updates via SMS. The script requires API keys for Alpha Vantage and News API, as well as a Twilio account to send SMS messages.
