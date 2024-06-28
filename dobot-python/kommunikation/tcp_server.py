import os
import sys
import socket
import json
sys.path.insert(0, os.path.abspath('.'))

from datenbank.write_database import insert_data

# Klasse für den TCP Server
class TCPServer:

    # Initialisierung des Servers
    def __init__(self, port):
        self.host = socket.gethostbyname(socket.gethostname())  # Automatisch die lokale IP holen
        self.port = port
        self.status = 0

    # Funktion, um die Verbindung zu starten
    def runConnection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(2)
            print(f"Connection established on host {self.host} and port {self.port}")
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        data = conn.recv(2048)
                        if not data:
                            print("No data sent. Ending connection.")
                            break
                        try:
                            received_data = json.loads(data.decode())
                            print("Received data:", received_data)
                            insert_data(received_data)
                        except json.JSONDecodeError:
                            print("Received non-JSON data:", data.decode())
                        conn.sendall(b"Server received the data.")

    # Funktion, um den Status zu setzen
    def setStatus(self, status):
        self.status = status

    # Funktion, um den Status zu holen
    def getStatus(self):
        return str(self.status)

# Hauptfunktion
def main():
    server = TCPServer(65432)
    print(f"Server startet auf {server.host}:{server.port}")
    print("TCP Server initialisiert...")
    try:
        while True:
            server.runConnection()
    except KeyboardInterrupt:
        print("Programm durch Benutzer gestoppt")

if __name__ == "__main__":
    main()
