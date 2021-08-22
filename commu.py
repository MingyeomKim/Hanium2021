import socket as sc
from time import sleep

HOST_1 = '110.165.16.23'
HOST_2 = '0.0.0.0'
PORT_1 = 1004
PORT_2 = 31004

# HOST_1 == 클라, 2번은 서버

socket_1 = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
socket_2 = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
socket_2.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)

socket_1.connect((HOST_1, PORT_1))

socket_2.bind((HOST_2, PORT_2))
socket_2.listen()

client, addr = socket_2.accept()

while True: 
    # 시그널 받기
    signal = socket_1.recv(8)

    # add 시그널은 이름과 데이터 받음
    if signal.decode() == 'add':
        # 라즈베리파이로 add 시그널 전송
        client.sendall(signal)

        # app.py에서 이름 받아오고 라파로 전송
        name = socket_1.recv(64)
        print(len(name.decode('utf-8')))
        client.sendall(name);sleep(0.01)

        # app.py에서 인코딩한 데이터 받아오고 라파로 전송
        data = socket_1.recv(4096)
        print(len(data.decode()))
        client.sendall(data)

    # open 시그널은 문 열기
    elif signal.decode() == 'open':
        # 라파로 시그널 전송
        client.sendall(signal)

    # remove 시그널은 라파에 저장된 정보 삭제하는 시그널
    elif signal.decode() == 'remove':
        # 라파에 삭제 시그널 전송
        client.sendall(signal)

        # app.py에서 받아온 라파에서 삭제할 이름을 라파로 전송
        name = socket_1.recv(64)
        client.sendall(name)