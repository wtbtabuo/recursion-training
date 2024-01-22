import socket
import json
import secrets

registered_user = {}

def handle_client_connection(client_socket):
    try:
        # ヘッダーの受信（固定32バイト）
        data = client_socket.recv(4096)
        if not data:
            return  # データがない場合は処理を終了

        # データの処理
        decoded_data = json.loads(data.decode())
        header = decoded_data.get('header')
        body = decoded_data.get('body')
        
        # 新規チャットルーム作成時
        if header.get('state') == 0:
            user_name = body.get('payload')
            room_name = body.get('room_name')
            if len(user_name) != 0 and len(room_name) != 0: 
                token = generate_token()

                registered_user[user_name] = token
                response = {
                    "status_code": 200,
                    "token": token
                }

                client_socket.sendall(json.dumps(response).encode())

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()
        print('connection closed')

def generate_token(length=32):
    return secrets.token_hex(length)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('127.0.0.1', 9002))
    server.listen(5)
    print("Server listening on port 9002")

    while True:
        client_sock, address = server.accept()
        print(f"Accepted connection from {address}")
        handle_client_connection(client_sock)

if __name__ == "__main__":
    start_server()
