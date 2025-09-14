import os
import requests

CMC_API_KEY = os.getenv("CMC_PRO_API_KEY")


def get_token_price(coin: str):
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": CMC_API_KEY
    }
    params = {
        "symbol": coin.upper(),
        "convert": "USD"
    }

    response = requests.get(url, headers=headers, params=params, timeout=5)

    if response.status_code != 200:
        return None

    data = response.json()
    try:
        price = data["data"][coin.upper()]["quote"]["USD"]["price"]
    except (KeyError, TypeError):
        return None

    return {
        "coin": coin.lower(),
        "currency": "usd",
        "price": price
    }