import socket

def ip_address_input():
    while True:
        ip_address = input('サーバーのIPアドレスを入力してください: ')
        if len(ip_address) == 0:
            print('入力は必須です。')
        else:
            break
    return ip_address

def user_inputs():
    # 新規チャット作成 or 既存チャット入室
    while True:
        init_operation = input('1か2を入力してください。\n新規のチャットルームを作成する: 1 / 既存のチャットルームに入る: 2\n')
        if init_operation not in ['1', '2']:
            print('1か2を入力してください')
        else:
            operation = 0 if init_operation == "1" else 1
            break

    # チャットルーム名入力
    while True:
        room_name = input('チャットルーム名を入力してください: ')
        if len(room_name) == 0:
            print('入力は必須です')
        else:
            break       

    # ユーザー名入力
    while True:
        user_name = input('ユーザー名を入力してください: ')
        if len(user_name) == 0:
            print('入力は必須です')
        else:
            break       

    return operation, room_name, user_name


def create_connection(connection_type):
    if connection_type == 'TCP':
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    elif connection_type == 'UDP':
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return sock
