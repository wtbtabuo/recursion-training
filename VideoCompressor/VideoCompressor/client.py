import json
import os
import tkinter.filedialog

from lib import utils

FILE_PATH = os.getcwd() # mp4ファイルが存在するディレクトリを指定する。

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

    def send_str_messages(self, data):
        user_input = json.dumps(data)
        self.client_socket.sendto(user_input.encode(), (self.address, self.port))

    def send_bin_messages(self, data):
        self.client_socket.sendto(data, (self.address, self.port))

    def receive_messages(self):
        while True:
            data, address = self.client_socket.recv(4096)
            if data:
                data = data.decode()
                print(json.dumps(data))

    def choose_and_check_mp4_file(self):
        # アップロードするファイル選択と、ファイルサイズが4GB以下かどうかのバリデーション
        while True:
            target_file = tkinter.filedialog.askopenfilename(
                initialdir=FILE_PATH,
                filetypes=[("mp4ファイル", "*.mp4")]
                )
            if not target_file:
                print('ファイルを選択してください')
                continue

            file_size = os.path.getsize(target_file)
            if file_size > 4 * 1024 * 1024 * 1024:
                print('ファイルサイズが4GBを超えています。')
                continue
            else:
                pass

            return target_file, file_size
    
    def generate_tcp_packet(self, path, size):
        data = {
            'file_name': path.split('/')[-1],
            'file_size': size
        }
        self.send_str_messages(data)
    
        with open(file_path, 'rb') as file:
            while True:
                data = file.read(1400)
                if not data:
                    break
                self.send_bin_messages(data)
        print('送信完了しました')

if __name__ == '__main__':
    client = Client()
    try:
        client.connect()
        file_path, file_size = client.choose_and_check_mp4_file()
        if file_path and file_size:
            client.generate_tcp_packet(file_path, file_size)
        client.receive_messages()
    finally:
        client.disconnect()
    