import socket

def main():
    host = '127.0.0.1'  # サーバーのホスト名
    port = 65432        # サーバーのポート

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        user_input = input("Enter your message: ")  # ユーザーからの入力を受け取る
        s.sendall(user_input.encode())
        data = s.recv(1024)

    print(f'Received: {data.decode()}')

if __name__ == "__main__":
    main()
