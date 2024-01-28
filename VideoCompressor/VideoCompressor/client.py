import json
import tkinter.filedialog

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

    def send_messages(self, data):
        user_input = json.dumps(data)
        self.client_socket.sendto(user_input.encode(), (self.address, self.port))

    def receive_messages(self):
        while True:
            data, address = self.client_socket.recv(4096)
            if data:
                data = data.decode()
                print(json.dumps(data))

    def split_packt(self, data, packet_size=1400):
        # データをパケットサイズに分割して送信
        for i in range(0, len(data), packet_size):
            packet = data[i:i+packet_size]
            self.send_messages(packet)
    @staticmethod
    def upload_mp4_fine():
        init_dir = '/mnt/c/Users/keita/Downloads/'
        target_file = tkinter.filedialog.askopenfilename(
            initialdir=init_dir,
            filetypes=[("mp4ファイル", "*.mp4")]
            )
        return target_file
if __name__ == '__main__':
    client = Client()
    try:
        client.connect()
        mp4_data = client.upload_mp4_fine()
        print(len(mp4_data))
        # client.split_packt(user_input)
        # client.receive_messages()
    finally:
        client.disconnect()
    