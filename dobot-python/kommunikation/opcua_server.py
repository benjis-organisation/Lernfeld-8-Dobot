# # OPCUA-Server 
# # by Hubert Vey 2021

# # Beschreibung:
# # https://github.com/FreeOpcUa/python-opcua/issues/803
# # https://github.com/FreeOpcUa/python-opcua/blob/master/examples/server-example.py


# #from opcua import Server
# import asyncio
# import asyncua

# from asyncua import ua, Server
# from asyncua.ua import ObjectIds

# from datetime import datetime
# import board
# import time
# import netifaces as ni #used for getting the ip address
# #(installieren via "sudo apt install python3-netifaces")

# # Sensor-Library vom Hersteller Adafruit
# import adafruit_dht

# #GPIOs konfigurieren
# import RPi.GPIO as GPIO


# async def main():
#     # Zählweise der Pins festlegen
#     GPIO.setmode(GPIO.BCM)
#     GPIO.setwarnings(False)
#     sensorPin=4
#     luefterPin=13

#     interface = 'wlan0'

#     #GPIO Eingänge festlegen
#     GPIO.setup(sensorPin, GPIO.IN)

#     #GPIO Ausgänge festlegen
#     GPIO.setup(luefterPin, GPIO.OUT)

#     # Device für Sensor 
#     dhtDevice = adafruit_dht.DHT22(board.D4, use_pulseio=False)

#     #Server Objekt anlegen und IP/Ports angeben
#     server=Server()
#     await server.init()

#     #Get the ip address
#     IPV4_Address = ni.ifaddresses(interface)[ni.AF_INET][0]['addr']
#     url="opc.tcp://"+IPV4_Address+":4840"
#     server.set_endpoint(url)


#     # Securityeinstellung "keine Sicherheit" für Clients angeben
#     # kann auch weggelassen werden
#     server.set_security_policy(
#     [
#         ua.SecurityPolicyType.NoSecurity
#     ])

#     # setup our own namespace, not really necessary but should as spec
#     uri="http://examples.freeopcua.github.io"
#     addspace=await server.register_namespace(uri)

#     # create a new node type we can instantiate in our address space
#     dev = await server.nodes.base_object_type.add_object_type(addspace, "FBS-Platine")
#     await (await dev.add_variable(addspace, "sensor", 1.0)).set_modelling_rule(True)
#     # await (await dev.add_variable(addspace, "luefter", 0)).set_modelling_rule(True)
#     await (await dev.add_variable(addspace, "time", datetime.utcnow())).set_modelling_rule(True)
#     await (await dev.add_variable(addspace, "humidity", 1.0)).set_modelling_rule(True)

#     # First a folder to organise our nodes
#     myfolder = await server.nodes.objects.add_folder(addspace, "Raspi")
#     # instanciate one instance of our device
#     mydevice = await myfolder.add_object(addspace, "FBS-Platine", dev)
    
#     # get proxy to child-elements
#     sensor = await mydevice.get_child(
#         [f"{addspace}:sensor"]
#     )    
#     # luefter = await mydevice.get_child(
#     #     [f"{addspace}:luefter"]
#     # )
#     time = await mydevice.get_child(
#         [f"{addspace}:time"]
#     )  
#     humidity = await mydevice.get_child(
#         [f"{addspace}:humidity"]
#     )

     
#     # make Variable writable from client
#     # await luefter.set_writable()    

#     #OPCUA-Server starten

#     async with server:   
#         print("Server startet auf {}",format(url))


#         #GPIOS der Schalter in einer Dauerschleife ausgeben
#         #Liste/Array und Flag definieren

#         while True:
#             #Zeit ermitteln
#             TIME = datetime.utcnow()

#             # Temperatur messen
#             try:
#                 # Print the values to Console
#                 temperature_c = dhtDevice.temperature
#                 temperature_f = temperature_c * (9 / 5) + 32
#                 humidity_e = dhtDevice.humidity
#                 print(
#                     "Temp: {:.1f} F / {:.1f} C    Humidity: {}%  Zeit:{:s}".format(
#                     temperature_f, temperature_c, humidity_e, TIME.strftime("%d-%b-%Y (%H:%M:%S.%f)")
#                     )
#                 )
#                 #OPCUA-Nodes setzen
#                 await sensor.write_value(temperature_c)
#                 await time.write_value(TIME)
#                 await humidity.write_value(humidity_e)
            
#                 ### Luefter-Flag abfragen
#                 # if (await luefter.read_value() == 1):
#                 #     print("Lüfter wurde über OPCUA angeschaltet")
#                 #     # physikalischen Lüfter einschalten
#                 #     GPIO.output(luefterPin,GPIO.HIGH)
#                 # else:
#                 #     GPIO.output(luefterPin,GPIO.LOW)
 
#             except RuntimeError as error:
#                 # Errors happen fairly often, DHT's are hard to read, just keep going
#                 print(error.args[0])
#                 await asyncio.sleep(2.0)
#                 continue
#             except Exception as error:
#                 dhtDevice.exit()
#                 raise error        
        
#             await asyncio.sleep(2.0)

# if __name__ == "__main__":
#     asyncio.run(main())