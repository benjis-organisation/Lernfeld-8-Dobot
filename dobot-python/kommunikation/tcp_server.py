# echo-server.py
import socket
import keyboard


class TCPServer:
    """TCP Socket Objekt für eine serverseitige TCP-Verbindung"""

    def __init__(self, host, port):
        """
        Host und Port werden zur Initialisierung der Klasse übergeben:
            -> Host: String, Standard loopback interface address (localhost - 127.0.0.1)
            -> Port Integer, Port to listen on (non-privileged ports are > 1023)
        """
        self.host = host
        self.port = port
        self.status = 0

    def getHelp(self):
        """Hilfeausgabe und Erklärungen zur Klasse / Methoden"""
        return print(help(TCPServer))

    def runConnection(self):
        """
        socket.socket zum Initialisieren einer Socketverbindung, with verhindert,
        dass mit s.close() die Verbindung geschlossen werden muss
        Parameter:
            > socket.AF_INET = IPv4 Adressbereich
            > socket.SOCK_STREAM = default / TCP-Verbindung (SOCK_DGRAM = UDP)
        bind() = Übergibt dem Socket eine IP und Portnummer
        listen() = Aktiviert den Server für Verbindungen über den Port
        accept() = Blockiert weitere Codeausführung und wartet auf eine Verbindung.
                   Bei einer Verbindung wird ein neues Socket Objekt zur Kommunikation mit dem Client erstellt.
        recv() = Eingehenden Daten vom Client
        sendall() = Daten an Client senden
        """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen(2)
            print(f"Connection established on host {self.host} and port {self.port}")
            while True:
                try:
                    conn, addr = s.accept()
                    with conn:
                        print(f"Connected by {addr}")
                        while True:
                            data = conn.recv(2048)
                            string = data.decode()
                            print("Data send: " + string)
                            if string == 'endServerConnection':
                                self.setStatus(1)
                            if not data:
                                print("No data send. Ending connection.")
                except KeyboardInterrupt:
                    print("Server is shutting down...")
                    s.close()
                    break
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(2048)
                    string = data.decode()
                    print("Data send: " + string)
                    if string == 'endServerConnection':
                        self.setStatus(1)
                    if not data:
                        print("No data send. Ending connection.")
                        conn.close()
                        break
                    conn.sendall(b'Server hat den Aufruf erhalten.')

    def setStatus(self, status):
        self.status = status

    def getStatus(self):
        return str(self.status)

def main():
    server = TCPServer("192.168.163.185", 65432)
    #server.getHelp()
    print("""
    TCP Server initialisiert.
    """)
    while True:
        server.runConnection()
        print("Server Status: " + str(server.getStatus()))
        if server.getStatus() == '1':
            print("Exit Programm...")
            break


if __name__ == "__main__":
    main()
