import socket
import json
import secrets
import threading

from lib.utils import create_connection

class Server:
    def __init__(self):
        self.registered_user = {}
        self.exist_chat_room = []

        self.address = '127.0.0.1'
        self.tcp_port = 9002
        self.udp_port = 9003

    def handle_client_connection(self, client_socket, address):
    
        # ヘッダーの受信（固定32バイト）
        data = client_socket.recv(4096)
        if not data:
            return False# データがない場合は処理を終了
        
        # データの処理
        decoded_data = json.loads(data.decode())
        header = decoded_data.get('header')
        body = decoded_data.get('body')

        room_name = body.get('room_name')
        operation = header.get('operation')
        state = header.get('state')
        room_name = body.get('room_name')
        user_name = body.get('user_name')

        # ipアドレスとユーザー名でキー作成
        address_str = "{}:{}".format(address[0], user_name)

        try:
            # チャットルーム新規作成時
            if operation == 0:
                # チャットルームが存在しないことの確認
                assert room_name not in self.exist_chat_room
                self.exist_chat_room.append(room_name)
            # 既存チャット入室時
            elif operation == 1:
                # チャットルームが既存のものか確認
                assert room_name in self.exist_chat_room 

            # ユーザー名が登録済みじゃないか確認
            assert address_str not in self.registered_user.keys()

            self.registered_user[address_str] = {}
            # トークンとユーザーを紐づけ
            token = Server.generate_token()
            self.registered_user[address_str]['token'] = token
            # ユーザーステータスを登録
            self.registered_user[address_str]['is_host'] = True if state == 0 else False

            response = {
                "status_code": 200,
                "token": token
            }
            client_socket.sendall(json.dumps(response).encode())

        except:
            response = {
                'status_code': 500,
                'message': 'チャットルームネームが不正です'
                }
            client_socket.sendall(json.dumps(response).encode())
        finally:
            client_socket.close()
    @staticmethod
    def generate_token(length=32):
        return secrets.token_hex(length)

    def start_server(self):
        server = create_connection('TCP')
        server.bind((self.address, self.tcp_port))
        server.listen(5)
        print("Server Start listening")

        try:
            while True:
                client_sock, address = server.accept()
                if client_sock and address:
                    print(f"Accepted connection from {address}")
                    self.handle_client_connection(client_sock, address)

        finally:  
            print('server stopped')  
            server.close()
    def start_chat(self):
        server = create_connection('UDP')
        server.bind((self.address, self.udp_port))

        clients = set()
        try:
            while True:
                data, address = server.recvfrom(4096)

                if data: 
                    try:
                        data = json.loads(data.decode())
                        address_str = "{}:{}".format(address[0], data['body']['user_name'])
                        is_host = self.registered_user[address_str]['is_host']
                        room_name = data['body']['room_name']
                        clients.add(address)

                        # アドレスが登録済みで、トークンがipアドレスと合致しているか確認
                        assert address_str in self.registered_user.keys()
                        assert data['body']['token'] == self.registered_user[address_str]['token']
                        
                        # クライアントからの退出メッセージではないか確認
                        assert data.get('body').get('message') != 'exit'
                        for client in clients:
                            if client != address:
                                data = json.dumps(data)
                                server.sendto(data.encode(), client)
                    except AssertionError:
                        if is_host:
                            del self.registered_user[address_str]
                            self.exist_chat_room.remove('{}'.format(room_name))
                            data['body']['message'] = 'host exited'
                        else:
                            data['body']['message'] = '{} exited'.format(data['body']['user_name'])
                        data = json.dumps(data).encode()
                        for client in clients:
                            server.sendto(data, client)
                        break
        finally:
            server.close()

if __name__ == "__main__":
    server = Server()

    start_server= threading.Thread(target=server.start_server)
    start_server.start()

    start_chat= threading.Thread(target=server.start_chat)
    start_chat.start()

