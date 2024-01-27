try:
    while True:
        my_message = input()
        if my_message != 'exit':
            continue
        else:
            break
finally:
    print('succeed')