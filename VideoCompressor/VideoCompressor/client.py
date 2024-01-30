import json
import os
import tkinter.filedialog

from lib import utils

# mp4ファイルが存在するディレクトリを指定する。
current_dir = os.getcwd() 
# print(os.path.join(parent_dir, 'input'))
FILE_PATH = os.path.join(current_dir, 'input')

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
        self.client_socket.sendall(user_input.encode())

    def send_bin_messages(self, data):
        self.client_socket.sendall(data)

    def receive_messages(self):
        while True:
            data = self.client_socket.recv(4096)
            if data:
                data = data.decode()
                return json.loads(data)

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
    
    def send_tcp_packet(self, path, size):
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
        print('送信中...')

        # ステータスコード200が返ってくるまで待機
        if self.receive_messages().get('status_code') == 200:
            print('動画の送信に成功しました')
        else:
            print('動画の送信に失敗しました')
        
    def choose_operation(self):
        operation = input("""
        動画処理について選択してください:
        1. 動画を圧縮する
        2. 動画の解像度を変更する
        3. 動画のアスペクト比を変更する
        4. 動画を音声に変換する
        5. 指定した時間範囲でGIF、若しくはWEBMを作成
        選択: """)
        while True:
            if int(operation) not in [1, 2, 3, 4, 5]:
                print('1～5を入力して下さい')
            else:
                break
        
        if int(operation) == 1:
            req = {'operation_id': 1}
            self.send_str_messages(req)
        
if __name__ == '__main__':
    client = Client()
    try:
        client.connect()
        file_path, file_size = client.choose_and_check_mp4_file()
        client.send_tcp_packet(file_path, file_size)
        client.choose_operation()
    finally:
        client.disconnect()
    