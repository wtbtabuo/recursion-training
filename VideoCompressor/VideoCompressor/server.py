import json

from lib import utils

class Server:
    def __init__(self):
        self.address = '127.0.0.1'
        self.port = 9002
    
    def connect(self):
        self.server_socket = utils.create_connection('TCP')
        self.server_socket.bind((self.address, self.port))
        self.server_socket.listen(5)
        print('server listening')
    
    def disconnect(self):
        self.server_socket.close()
        print('connection closed')

    def receive_packet(self):
        while True:
            client_socket, address = self.server_socket.accept()
            if address:
                print('connection from {}'.format(address))

            data = client_socket.recv(1400)
            if data:
                decoded_data = data.decode()
                print(json.loads(decoded_data))

if __name__ == '__main__':
    server = Server()
    try:
        server.connect()
        server.receive_packet()
    finally:
        server.disconnect()