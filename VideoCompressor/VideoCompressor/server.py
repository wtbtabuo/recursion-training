import json
import os
import subprocess
import tempfile

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

    def save_bytes_to_tempfile(self):
        # 一時的にバイトデータを動画データに変換
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        temp_file.write(self.file_data)
        temp_file.close()
        return temp_file.name
    
    def delete_tempfile(self, file_path):
        # 一時ファイルを削除
        os.remove(file_path)

    def handle_order(self):
        while True:
            data = self.client_socket.recv(1400)
            if data:
                formed_data = json.loads(data.decode())

                # インスタンスに存在するバイトデータをmp4に一時的に変換
                vide_file_path = self.save_bytes_to_tempfile()

                if formed_data.get('operation_id') == 1:
                    self.compress_video(vide_file_path)

                self.delete_tempfile(vide_file_path)
                

    def get_vide_info(self):
        video_path = self.save_bytes_to_tempfile()
        print(video_path)
        cmd = [
                'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                '-show_entries', 'stream=width,height,bit_rate',
                '-of', 'json', video_path
            ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return json.loads(result.stdout)
    
    def compress_video(self, file_path):
        video_info = self.get_vide_info()
        print(video_info)


if __name__ == '__main__':
    server = Server()
    try:
        server.connect()
        server.receive_video_packet()
        server.handle_order()
    finally:
        server.disconnect()