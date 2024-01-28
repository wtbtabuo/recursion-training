import json

from lib import utils

class Client:
    def __init__(self):
        self.address = '127.0.0.1'
        self.port = 9002

    def connect(self):
        self.client_socket = utils.create_connection('TCP')
        self.client_socket.connect((self.address, self.port))
        print('connection built')

    def disconnect(self):
        self.client_socket.close()
        print('connection closed')

    def send_messages(self):
        user_input = input('テスト入力です: ')
        user_input = json.dumps(user_input)
        self.client_socket.sendto(user_input.encode(), (self.address, self.port))

    def receive_messages(self):
        while True:
            data, address = self.client_socket.recv((self.address, self.port))
            if data:
                data = data.decode()
                print(json.dumps(data))
if __name__ == '__main__':
    client = Client()
    try:
        client.connect()
        client.send_messages()
    finally:
        client.disconnect()
    