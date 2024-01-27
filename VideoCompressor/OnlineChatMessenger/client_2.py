import json
import threading
import sys

from lib.utils import user_inputs
from lib.utils import create_connection

class Client:
    def __init__(self):
        self.address = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
        self.tcp_port = 9002
        self.udp_port = 9003
        self.token = None
        self.data = {
            'header': {},
            'body': {}
        }
        self.is_exited = False

    def generate_tcp_packet(self, room_name, operation, state, user_name):
        header = self.data['header']
        header['room_name_size'] = len(room_name)
        header['operation'] = operation
        header['state'] = state
        header['user_name_size'] = len(user_name)

        body = self.data['body']
        body['room_name'] = room_name
        body['user_name'] = user_name
        
        return 

    def init_operation(self):
        # TCPコネクション
        sock = create_connection('TCP')
        sock.connect((self.address, self.tcp_port))

        try:
            # ユーザー入力
            operation, room_name, user_name = user_inputs()
            
            # oepration=0 -> チャットルーム新規作成, state=0 -> ホストユーザー
            # oepration=1 -> 既存チャット入室, state=1  -> 一般ユーザー
            state = operation 

            # tcpパケットのインスタンス作成
            self.generate_tcp_packet(room_name, operation, state, user_name)

            data = json.dumps(self.data)
            sock.sendall(data.encode())

            # サーバーからのレスポンスを待つ
            while True:
                data = sock.recv(255)
                if data:
                    break
            
            response = json.loads(data.decode())
            if response.get('status_code') == 200 and state == 0: 
                self.token = response['token']
                print("新規チャットルーム'{}'が作成されました".format(room_name))
                return True
            elif response.get('status_code') == 200 and state == 1: 
                self.token = response['token']
                print("チャットルーム'{}'に入室しました".format(room_name))
                return True
            elif response.get('status_code') == 500:
                print(response.get('message'))
                return False       

        finally:
            sock.close()

    def generate_udp_packet(self, message):
        # tcpコネクション作成時の余計な部分を削除
        if 'operation' in self.data['header']:
            del self.data['header']['operation']
        if 'state' in self.data['header']:
            del self.data['header']['state']

        self.data['header']['token_size'] = len(self.token)
        self.data['body']['token'] = self.token
        self.data['body']['message'] = message

        return 

    def receive_messages(self, sock):
        while True:
            try:
                data, address = sock.recvfrom(4094)
                if data:
                    data = json.loads(data.decode())
                    assert data['body']['message'] != 'host exited'
                    assert data['body']['message'] != '{} exited'.format(self.data['body']['user_name'])
                    name = data['body']['user_name']
                    message = data['body']['message']
                    sys.stdout.write('\r' + ' ' * (len(self.data['body']['user_name']) + 2))  # 現在の行をクリア
                    sys.stdout.write('\r{}: {}\n'.format(name, message))  # 受信メッセージを表示
                    sys.stdout.write('{}: '.format(self.data['body']['user_name']))  # プロンプトを再表示
                    sys.stdout.flush()
            except AssertionError:
                print('\rチャットルームが削除されました')
                break

    def send_messages(self, sock):
        try:
            while True:
                my_message = input("{}: ".format(self.data['body']['user_name']))
                if my_message != 'exit':
                    self.generate_udp_packet(my_message)
                    sock.sendto(json.dumps(self.data).encode(), (self.address, self.udp_port))
                else:
                    self.is_exited = True
                    self.generate_udp_packet("exit")
                    sock.sendto(json.dumps(self.data).encode(), (self.address, self.udp_port))
                    break
        finally:
            sock.close()

if __name__ == "__main__":
    # 初期設定操作
    client = Client()
    while True:
        if client.init_operation():
            # スレッドでメッセージの送受信を開始
            sock = create_connection('UDP')
            threading.Thread(target=client.receive_messages, args=(sock,)).start() 
            client.send_messages(sock)
        
        if client.is_exited:  # チャットルームから退出した場合
            client.is_exited = False  # フラグをリセットしてループを続ける
            continue