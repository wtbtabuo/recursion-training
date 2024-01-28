import json
import time
from lib import utils



class Server:
    def __init__(self):
        self.address = '127.0.0.1'
        self.port = 9002
        self.file_name = None
        self.file_data = b''
    
    def connect(self):
        self.server_socket = utils.create_connection('TCP')
        self.server_socket.bind((self.address, self.port))
        self.server_socket.listen(5)
        print('server listening')
    
    def disconnect(self):
        self.server_socket.close()
        print('connection closed')

    def receive_packet(self):
        client_socket, address = self.server_socket.accept()
        if address:
            print('connection from {}'.format(address))

        while True:
            data = client_socket.recv(1400)
            if not data:
                break

            if self.file_name is None:
                meta_data = json.loads(data.decode())
                if meta_data.get('file_name'):
                    self.file_name = meta_data['file_name']
            else:
                self.file_data += data

    def save_file(self):
        with open('copy'+self.file_name, 'wb') as f:
            f.write(self.file_data)

if __name__ == '__main__':
    server = Server()
    try:
        server.connect()
        server.receive_packet()
        server.save_file()
    finally:
        server.disconnect()