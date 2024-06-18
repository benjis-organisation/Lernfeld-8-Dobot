import asyncua
import netifaces as ni
import asyncio
import tkinter as tk
from tkinter import ttk

from asyncua import Client

async def main():
    interface = 'wlan0'
    url = "opc.tcp://192.168.255.127:4840"
    namespace = "http://examples.freeopcua.github.io"

    client = Client(url=url,timeout=10)

    await client.connect()

    nsidx = await client.get_namespace_index(namespace)
    print(f"Namespace Index for '{namespace}': {nsidx}")

    temperature = await client.nodes.root.get_child(["0:Objects", f"{nsidx}:Raspi", f"{nsidx}:FBS-Platine", f"{nsidx}:sensor"])
    humidity = await client.nodes.root.get_child(["0:Objects", f"{nsidx}:Raspi", f"{nsidx}:FBS-Platine", f"{nsidx}:humidity"])
    time = await client.nodes.root.get_child(["0:Objects", f"{nsidx}:Raspi", f"{nsidx}:FBS-Platine", f"{nsidx}:time"])
    
    while True:
        #root.mainloop()
        print("Sensor: " + str(await temperature.read_value()))
        print("Humidity: " + str(await humidity.read_value()))
        print("Zeit: " + str(await time.read_value()))
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
