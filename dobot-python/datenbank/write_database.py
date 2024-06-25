import pymongo
import time
from datetime import datetime
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from kommunikation.awattar_api import fetch_awattar_prices

# Verbindung zur MongoDB herstellen
prices = fetch_awattar_prices()
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Messdaten"]
humidityCollection = db["Feuchtigkeit"]
temperatureCollection = db["Temperatur"]
colorCollection = db["Farbwerte"]
energyCollection = db["Energiekosten"]

start_date = datetime.strptime('2024-06-25 23:00:00', '%Y-%m-%d %H:%M:%S')
end_date = datetime.strptime('2024-06-26 00:00:00', '%Y-%m-%d %H:%M:%S')

humidity = { "current_date": time.time(), "humidity": 50.1 }
temperature = { "current_date": time.time(), "temperature": 20.1 }
color = { "current_date": time.time(), "hex_code": "#ff8234"}

humidityCollection.insert_one(humidity)
temperatureCollection.insert_one(temperature)
colorCollection.insert_one(color)
energyCollection.insert_many(prices)