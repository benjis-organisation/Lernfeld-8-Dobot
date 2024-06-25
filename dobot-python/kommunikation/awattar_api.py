import requests
import json
from datetime import datetime

def fetch_awattar_prices():
    response = requests.get('https://api.awattar.de/v1/marketdata')
    data = response.json()
    prices = []

    for item in data['data']:
        start = datetime.fromtimestamp(item['start_timestamp'] / 1000)
        end = datetime.fromtimestamp(item['end_timestamp'] / 1000)
        prices.append({
            "Start": start,
            "End": end,
            "Marketprice": item['marketprice']
        })
        
    return prices