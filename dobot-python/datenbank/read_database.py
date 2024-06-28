import pymongo
import json
from bson import json_util

energiekosten_gesendet = False

# Verbindung zur MongoDB herstellen
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Messdaten"]
humidityCollection = db["Feuchtigkeit"]
temperatureCollection = db["Temperatur"]
colorCollection = db["Farbwerte"]
energyCollection = db["Energiekosten"]

# Funktion, um alle Daten aus einer Collection zu lesen
def read_collection(collection):
    return list(collection.find({}))

# Funktion, um alle Daten aus der Datenbank zu lesen und als JSON-String zurückzugeben
def get_all_data_as_json():
    
    global energiekosten_gesendet
    
    humidity_data = read_collection(humidityCollection)
    temperature_data = read_collection(temperatureCollection)
    color_data = read_collection(colorCollection)
    energy_data = read_collection(energyCollection) if not energiekosten_gesendet else []

    if energy_data:
        energiekosten_gesendet = True

    last_humidity_data = humidity_data[-1] if humidity_data else None
    last_temperature_data = temperature_data[-1] if temperature_data else None
    last_color_data = color_data[-1] if color_data else None

    all_data = {
        "Feuchtigkeit": last_humidity_data,
        "Temperatur": last_temperature_data,
        "Farbwerte": last_color_data,
        "Energiekosten": energy_data
    }

    return json.dumps(all_data, default=json_util.default)