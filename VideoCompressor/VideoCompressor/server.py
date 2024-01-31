import json
import os
import subprocess
import tempfile

from lib import utils
from lib import ffmpeg_cmds

# mp4ファイルを吐き出すディレクトリを指定
current_dir = os.getcwd() 
OUTPUT_DIR = os.path.join(current_dir, 'output')

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
                video_file_path = self.save_bytes_to_tempfile()

                if formed_data.get('operation_id') == 1: # 圧縮
                    self.compress_video(video_file_path)

                elif formed_data.get('operation_id') == 2: # 解像度変更
                    resolution_type = formed_data.get('resolution')
                    self.change_resolution(video_file_path, resolution_type)

                elif formed_data.get('operation_id') == 3: # アスペクト比変更
                    ratio= formed_data.get('ratio')
                    self.change_aspect_ratio(video_file_path, ratio)

                elif formed_data.get('operation_id') == 4:
                    mp3_file_name = self.file_name[:-4] + '.mp3'
                    output_vide_path = os.path.join(OUTPUT_DIR, mp3_file_name)
                    cmd = ffmpeg_cmds.extract_mp3(video_file_path, output_vide_path)
                    self.execute_commands(cmd)

                elif formed_data.get('operation_id') == 5:
                    video_type = 'gif' if formed_data.get('video_type') == str(1) else 'webm'
                    time_range = formed_data.get('timerange')
                    self.crop_and_covert_video(video_file_path, video_type, time_range)
                    
                self.delete_tempfile(video_file_path)

    def execute_commands(seld, cmd):
        try:
            subprocess.run(cmd, check=True)
            data = {'status_code': 200}
        except subprocess.CalledProcessError as e:
            print(e)
            data = {'status_code': 500}
        except Exception as e:
            data = {'status_code': 500}
        return data
    
    def get_vide_info(self):
        # 動画のwidth, height, bit_rateを出力
        video_path = self.save_bytes_to_tempfile()
        cmd = ffmpeg_cmds.get_vide_info(video_path)
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return json.loads(result.stdout)
    
    def compress_video(self, file_path):
        # 動画のbit_rateを元に、圧縮比率を決め手圧縮
        video_info = self.get_vide_info()
        bit_rate = int(video_info['streams'][0]['bit_rate']) 

        if bit_rate > 5000000: # ビットレートが5Mbpsを超える場合
            taraget_bite_rate = '2500k'
        elif bit_rate < 2000000:  # ビットレートが2Mbps未満の場合
            taraget_bite_rate = '1500k'
        else:
            taraget_bite_rate = str(bit_rate // 2) + 'k'

        out_put_path = os.path.join(OUTPUT_DIR, 'compressed_'+self.file_name,)

        cmd = ffmpeg_cmds.compress(file_path, out_put_path, taraget_bite_rate)
        result = self.execute_commands(cmd)
        self.client_socket.sendall(json.dumps(result).encode())

    def change_resolution(self, file_path, resolution):
        if resolution == 1:
            width, height = 1920, 1080  
        elif resolution == 2:
            width, height = 1280, 720  
        else:
            width, height = 720, 480 

        output_path = os.path.join(OUTPUT_DIR, f'{width}*{height}_'+self.file_name)

        cmd = ffmpeg_cmds.change_resolution(file_path, width, height, output_path)
        result = self.execute_commands(cmd)
        self.client_socket.sendall(json.dumps(result).encode())

    def change_aspect_ratio(self, file_path, ratio):
        video_info = self.get_vide_info()
        bit_rate = video_info['streams'][0]['bit_rate'] # 動画のビットレート取得

        out_put_path = os.path.join(OUTPUT_DIR, 'aspect_ratio_'+ratio+self.file_name,)

        cmd = ffmpeg_cmds.change_aspect_ratio(file_path, bit_rate, ratio, out_put_path)
        result = self.execute_commands(cmd)
        self.client_socket.sendall(json.dumps(result).encode())

    def crop_and_covert_video(self, file_path, video_type, time_range):
        out_put_path = os.path.join(OUTPUT_DIR, self.file_name[:-3]+f'{video_type}',)
        print(out_put_path)
        if video_type == 'gif':
            cmd = ffmpeg_cmds.convert_to_gif(file_path, time_range, out_put_path)
        elif video_type == 'webm':
            cmd = ffmpeg_cmds.convert_to_webm(file_path, time_range, out_put_path)
        result = self.execute_commands(cmd)
        self.client_socket.sendall(json.dumps(result).encode())

if __name__ == '__main__':
    server = Server()
    try:
        server.connect()
        server.receive_video_packet()
        server.handle_order()
    finally:
        server.disconnect()