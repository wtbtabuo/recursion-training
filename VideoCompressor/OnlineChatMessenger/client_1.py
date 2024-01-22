import socket
import json

def send_data(sock, server_address, room_name, operation, state, payload):
    # ヘッダーとボディをJSON形式で作成
    data = {
        "header": {
            "room_name_size": len(room_name),
            "operation": operation,
            "state": state,
            "payload_size": len(payload)
        },
        "body": {
            "room_name": room_name,
            "payload": payload
        }
    }

    # JSON形式の文字列に変換
    json_data = json.dumps(data)

    # データをバイト列にエンコードして送信
    sock.sendto(json_data.encode(), server_address)

def wait_res(sock):
    data = sock.recv(255)
    if not data:
        return
    print(json.loads(data.decode()))


# サーバーの接続設定
server_address = ('127.0.0.1', 9002)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)

# ユーザー入力
init_operation = input('1か2を入力してください。\n既存のチャットルームに入る: 1 / 新規のチャットルームを作成する: 2\n')
if init_operation not in ['1', '2']:
    print('1か2を入力してください')
else:
    try:
            
        operation = int(init_operation)
        state = 0  # 仮の状態設定
        room_name = input('チャットルーム名を入力してください。')
        payload = input('ユーザー名を入力してください。')

        # データの送信
        send_data(sock, server_address, room_name, operation, state, payload)

        # サーバーからのレスポンスを待つ
        while True:
            wait_res(sock)
    except:
        # ソケットのクローズ
        sock.close()
        print('connection closed')
