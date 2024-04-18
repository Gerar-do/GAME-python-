import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = "10.10.0.36"  # Cambiar a la IP del servidor
        self.port = 5555
        self.addr = (self.host, self.port)
        self.player_id = None

    def get_player_id(self):
        """
        :return: str
        """
        try:
            self.client.connect(self.addr)
            self.player_id = self.client.recv(2048).decode()
            return self.player_id
        except socket.error as e:
            return str(e)

    def send(self, data):
        """
        :param data: str
        :return: str
        """
        try:
            self.client.send(str.encode(data))
            reply = self.client.recv(2048).decode()
            return reply
        except socket.error as e:
            return str(e)
