from opcua import Server
from datetime import datetime
import time
import math

# Funktion, um den OPC UA Testserver zu starten
def run_opcua_test_server():
    server = Server()

    url = "opc.tcp://localhost:4840"
    server.set_endpoint(url)
    
    uri = "http://examples.freeopcua.github.io"
    idx = server.register_namespace(uri)

    raspi_obj = server.nodes.objects.add_object(idx, "Raspi")

    fbs_platine_obj = raspi_obj.add_object(idx, "FBS-Platine")

    temp_var = fbs_platine_obj.add_variable(idx, "sensor", 20.0)
    humidity_var = fbs_platine_obj.add_variable(idx, "humidity", 50.0)
    time_var = fbs_platine_obj.add_variable(idx, "time", 0)

    temp_var.set_writable()
    humidity_var.set_writable()
    time_var.set_writable()

    server.start()
    print(f"Server gestartet bei {url}")

    try:
        while True:
            time.sleep(1)
            current_time = int(time.time())
            temp_value = round(20.0 + 5.0 * math.sin(current_time), 1)
            humidity_value = round(50.0 + 10.0 * math.cos(current_time), 1)
            
            temp_var.set_value(temp_value)
            humidity_var.set_value(humidity_value)
            time_var.set_value(current_time)
    finally:
        server.stop()
        print("Server gestoppt")

if __name__ == "__main__":
    run_opcua_test_server()