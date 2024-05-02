
import random

from paho.mqtt import client as mqtt_client

broker = 'test.mosquitto.org'
port = 1883
topic = "temp/test/topic" 

client_id = f'subscribe-{random.randint(0, 100)}'

def connect_mqtt():
    def on_connect(mqttc, obj, flags, reason_code, properties):
        print("reason_code: " + str(reason_code))

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()