import json
import time
from lib import utils



class Server:
    def __init__(self):
        self.address = '127.0.0.1'
        self.port = 9002
        self.file_name = None
        self.file_size = 1
        self.file_data = b''
    
    def connect(self):
        self.server_socket = utils.create_connection('TCP')
        self.server_socket.bind((self.address, self.port))
        self.server_socket.listen(5)
        print('server listening')
    
    def disconnect(self):
        self.server_socket.close()
        print('connection closed')

    def receive_video_packet(self):
        client_socket, address = self.server_socket.accept()
        if address:
            print('connection from {}'.format(address))
            self.client_socket = client_socket

        try:
            while len(self.file_data) != self.file_size:
                data = client_socket.recv(1400)

                if self.file_name is None:
                    meta_data = json.loads(data.decode())
                    if meta_data.get('file_name'):
                        self.file_name = meta_data['file_name']
                        self.file_size = meta_data['file_size']
                else:
                    self.file_data += data
        finally:
            data = {'status_code': 200}
            client_socket.sendall(json.dumps(data).encode())
            print('動画の受信完了しました')

    def receive_order_packet(self):
        while True:
            data = self.client_socket.recv(1400)
            if data:
                print(json.loads(data.decode()))

if __name__ == '__main__':
    server = Server()
    try:
        server.connect()
        server.receive_video_packet()
        server.receive_order_packet()
    finally:
        server.disconnect()