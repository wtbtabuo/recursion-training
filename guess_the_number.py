import sys
import random

# 最小数の入力を促す
sys.stdout.buffer.write(b'What is the minimum number?\n')
sys.stdout.flush()
min_num = sys.stdin.buffer.readline().strip()

# 最大数の入力を促す
sys.stdout.buffer.write(b'What is the maximum number?\n')
sys.stdout.flush()
max_num = sys.stdin.buffer.readline().strip()

try:
    # バイト文字列をデコードして整数に変換
    max_num = int(max_num.decode())
    min_num = int(min_num.decode())

    # ランダムな数値を生成
    random_number = random.randint(min_num, max_num)
    
except ValueError:
    print("Please enter a valid number.")

try:
    # 推測する数値の入力を促す
    sys.stdout.buffer.write(b'type the random number between ' + str(min_num).encode() + b' and ' + str(max_num).encode() + b'\n')
    sys.stdout.flush()
    sys.stdout.buffer.write(b'you have 5 chances\n')
    sys.stdout.flush()

    for _ in range(4):
        # バイト文字列をデコードして整数に変換
        guess = sys.stdin.buffer.readline().strip()
        guess = int(guess.decode())
        
        # 推測した数値が正解かどうか判定
        if guess == random_number:
            sys.stdout.buffer.write(b'You guessed correctly!\n')
            break
        elif guess > random_number:
            sys.stdout.buffer.write(b'Your guess is too high, try again!\n')
            sys.stdout.flush()
        elif guess < random_number:
            sys.stdout.buffer.write(b'Your guess is too low, try again!\n')
            sys.stdout.flush()

    else:
        # 推測回数が5回を超えた場合
        sys.stdout.buffer.write(b'you have no more chances\n')
        sys.stdout.flush()  
except ValueError:
    print("Please enter a valid number.")
