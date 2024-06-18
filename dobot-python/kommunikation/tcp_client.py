import socket
import time


class TCPClient:
    def __init__(self, host, port):
        """
        Konstruktor der Client Klasse
        :param host: Hostadresse womit connected wird
        :param port: Port des Hosts für die TCP Verbindung
        """
        self.host = host
        self.port = port
        self.socket = None

    def setSocket(self, sock):
        """
        Setzt den socket Wert des Clients
        :param sock: Socket
        """
        self.socket = sock

    def sendData(self, data):
        """
        Verbindung zum Server steht, schicke Daten und bekomme Antwort
        :param data: Daten welche an den Server geschickt werden sollen (Leerstring zum Beenden)
        """
        msg = "Hallo, ich bin eine TCP Verbindung"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((self.host, self.port))
                s.sendall(data.encode())
                data = s.recv(2048).decode()
                print("Server: " + data)
        except Exception as e:
            print("Fehler:\n" + str(e))

        #print(f"Antwort Server: {self.socket.recv(2048).decode()}")



def main():
    client = TCPClient("192.168.255.44", 65432)

    print("Trying to send data:")
    counter = 1
    while counter < 6:
        if counter == 5:
            client.sendData("endServerConnection")
        else:
            client.sendData(f"Runde {counter}, warte 3 Sekunden")
        counter += 1
        time.sleep(3)

    print("Connection closed")


if __name__ == "__main__":
    main()
