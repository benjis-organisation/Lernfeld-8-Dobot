import pymongo
from datetime import datetime
import json

# Verbindung zur MongoDB herstellen
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Messdaten"]
humidityCollection = db["Feuchtigkeit"]
temperatureCollection = db["Temperatur"]
colorCollection = db["Farbwerte"]
energyCollection = db["Energiekosten"]

color_to_hex = {
    "red": "#FF0000",
    "green": "#00FF00",
    "blue": "#0000FF",
    "yellow": "#FFFF00"
}

def format_date(dt):
    return {"$date": dt.isoformat() + "Z"}

# Funktion, um die letzte gespeicherte Farbe aus der Datenbank zu lesen
def get_last_color():
    last_color = colorCollection.find_one(sort=[("current_date", pymongo.DESCENDING)])
    if last_color:
        return last_color["hex_code"]
    return None

# Funktion, um Daten in die Datenbank einzufuegen
def insert_data(data):
    if "sensor_data" in data:
        sensor_data = json.loads(data["sensor_data"])
        if "humidity" in sensor_data:
            humidity = {"current_date": datetime.now(), "humidity": sensor_data["humidity"]}
            humidityCollection.insert_one(humidity)
        if "temperature" in sensor_data:
            temperature = {"current_date": datetime.now(), "temperature": sensor_data["temperature"]}
            temperatureCollection.insert_one(temperature)

    if "color_detected" in data:
        new_color_hex = color_to_hex.get(data["color_detected"], None)
        if new_color_hex and new_color_hex != get_last_color():
            color = {"current_date": datetime.now(), "hex_code": new_color_hex}
            colorCollection.insert_one(color)

    if "awattar_prices" in data:
        for price in data["awattar_prices"]:
            energy = {
                "start": format_date(datetime.strptime(price["Start"], "%Y-%m-%d %H:%M:%S")),
                "end": format_date(datetime.strptime(price["End"], "%Y-%m-%d %H:%M:%S")),
                "marketprice": price["Marketprice"]
            }
            energyCollection.insert_one(energy)
