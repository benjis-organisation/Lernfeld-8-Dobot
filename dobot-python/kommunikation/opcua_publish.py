import time
import paho.mqtt.client as mqtt
broker="test.mosquitto.org"
port=1883
def on_publish(client, userdata, mid, reason_code, properties):            #create function for callback
    print("data published \n")
    pass

def on_connect(mqttc, obj, flags, reason_code, properties):
    print("reason_code: " + str(reason_code)) 

mqttc = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqttc.on_publish = on_publish
try:
    mqttc.connect("test.mosquitto.org", 1883)   #establish connection
except Exception as e:
    print(f"Failed to connect: {e.__context__}")
mqttc.on_connect = on_connect
mqttc.loop_start()

# Our application produce some messages
msg_info = mqttc.publish("FBS/LF8_Projekt/Zeit", "Hallo 11B392", qos=1)

#msg_info2 = mqttc.publish("vey/test/topic", "my message2", qos=1)

# Due to race-condition described above, the following way to wait for all publish is safer
msg_info.wait_for_publish()
#msg_info2.wait_for_publish()

mqttc.disconnect()
mqttc.loop_stop()                #publish