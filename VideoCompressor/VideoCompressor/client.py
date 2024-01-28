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

    def send_messages(self, data):
        user_input = json.dumps(data)
        self.client_socket.sendto(user_input.encode(), (self.address, self.port))

    def receive_messages(self):
        while True:
            data, address = self.client_socket.recv(4096)
            if data:
                data = data.decode()
                print(json.dumps(data))

    def split_packet(self, data, packet_size=1400):
        # データをパケットサイズに分割して送信
        packet_list = []
        for i in range(0, len(data), packet_size):
            packet = data[i:i+packet_size]
            packet_list.append(packet)
        return packet_list

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
            self.file = target_file
            file_size = os.path.getsize(target_file)
            if file_size > 4 * 1024 * 1024 * 1024:
                print('ファイルサイズが4GBを超えています。')
                continue
            else:
                self.file_size = file_size

            self.file_name = os.path.basename(target_file)
            return 
    
    def generate_tcp_packet(self, operation):
        if operation == 'init':
            data = {
                'file_name': self.file_name,
                'file_size': self.file_size
            }
            self.send_messages(data)
        
        else:
            packet_list = self.split_packet(self.file)
            for packet in packet_list:
                self.send_messages(packet)
        print('送信完了しました')

if __name__ == '__main__':
    client = Client()
    try:
        client.connect()
        client.choose_and_check_mp4_file()
        client.generate_tcp_packet(operation='init') # ファイルサイズデータを送信
        client.generate_tcp_packet(operation=None) # mp4ファイルを送信
        client.receive_messages()
    finally:
        client.disconnect()
    