import asyncio
import json
import socket
import os
from asyncua import Client
from datetime import datetime
from awattar_api import fetch_awattar_prices

color_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'color_detected.json')

# Funktion, um das datetime-Objekt in einen String umzuwandeln
def datetime_converter(o):
    if isinstance(o, datetime):
        return o.__str__()

# Funktion, um die Sensorwerte aus dem OPC UA Server zu holen
async def get_sensor_values(client, nsidx):
    temperature_node = await client.nodes.root.get_child(["0:Objects", f"{nsidx}:Raspi", f"{nsidx}:FBS-Platine", f"{nsidx}:sensor"])
    humidity_node = await client.nodes.root.get_child(["0:Objects", f"{nsidx}:Raspi", f"{nsidx}:FBS-Platine", f"{nsidx}:humidity"])
    time_node = await client.nodes.root.get_child(["0:Objects", f"{nsidx}:Raspi", f"{nsidx}:FBS-Platine", f"{nsidx}:time"])

    temperature_value = await temperature_node.read_value()
    humidity_value = await humidity_node.read_value()
    time_value = await time_node.read_value()

    sensor_data = {
        "temperature": temperature_value,
        "humidity": humidity_value,
        "time": time_value
    }

    sensor_data_json = json.dumps(sensor_data, default=datetime_converter)
    return sensor_data_json

#  Klasse für den TCP Client
class TCPClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def send_data(self, data):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(json.dumps(data).encode())
                response = s.recv(2048).decode()
                print("Server response: " + response)
        except Exception as e:
            print("Error:\n" + str(e))

# Hauptfunktion
async def main():
    # IP Adresse des Servers muss angepasst werden
    url = "opc.tcp://localhost:4840"
    namespace = "http://examples.freeopcua.github.io"

    client = Client(url=url, timeout=10)
    await client.connect()

    nsidx = await client.get_namespace_index(namespace)
    print(f"Namespace Index for '{namespace}': {nsidx}")

    # IP Adresse des Servers muss angepasst werden
    tcp_client = TCPClient("192.168.0.34", 65432)

    awattar_prices = fetch_awattar_prices()
    data_to_send = {
        "awattar_prices": awattar_prices
    }

    first_run = True

    while True:
        sensor_data = await get_sensor_values(client, nsidx)

        if first_run:
            data_to_send["sensor_data"] = sensor_data
            first_run = False
        else:
            data_to_send = {"sensor_data": sensor_data}

        try:
            with open(color_file_path, 'r') as file:
                color_data = json.load(file)
                print(f"Read color data from file: {color_data}")
                data_to_send["color_detected"] = color_data["color_detected"]
        except FileNotFoundError:
            print(f"Color file not found at path: {color_file_path}")
            data_to_send["color_detected"] = "unknown"
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from color file: {e}")
            data_to_send["color_detected"] = "unknown"
        except KeyError:
            print(f"Key 'color_detected' not found in the color data")
            data_to_send["color_detected"] = "unknown"

        print("Data to send:", data_to_send)

        await tcp_client.send_data(data_to_send)

        if not first_run:
            # Entfernet die awattar_prices aus dem JSON nach dem ersten Senden
            data_to_send.pop("awattar_prices", None)

        await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(main())
