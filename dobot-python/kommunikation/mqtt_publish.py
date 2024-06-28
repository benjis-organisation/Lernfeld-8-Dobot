import time
import paho.mqtt.client as mqtt
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from datenbank.read_database import get_all_data_as_json

broker="test.mosquitto.org"
port=1883

# Funktion, die aufgerufen wird, wenn die Daten erfolgreich publiziert wurden
def on_publish(client, userdata, mid, reason_code, properties):
    print("data published \n")
    pass

# Funktion, die aufgerufen wird, wenn die Verbindung zum Broker hergestellt wurde
def on_connect(mqttc, obj, flags, reason_code, properties):
    print("reason_code: " + str(reason_code)) 

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish

try:
    mqttc.connect("test.mosquitto.org", 1883)
except Exception as e:
    print(f"Failed to connect: {e.__context__}")
mqttc.on_connect = on_connect
mqttc.loop_start()

try:
    while True:
        data_json = get_all_data_as_json()
        
        print(data_json)
        msg_info = mqttc.publish("FBS/LF8_Projekt/JSON", data_json)
        
        time.sleep(5)
except KeyboardInterrupt:
    # Tastaturunterbrechung (CTRL+C) wird verwendet, um die Schleife zu beenden
    print("Programm durch Benutzer gestoppt")
msg_info.wait_for_publish()

mqttc.disconnect()
mqttc.loop_stop()