import socket as sc
import datetime

HOST_3 = '0.0.0.0'
PORT_3 = 31005
path = 'C:\\Users\\Administrator\\Desktop\\final\\Temperature.txt'

socket_3 = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
socket_3.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)

socket_3.bind((HOST_3, PORT_3))
socket_3.listen()

client, addr = socket_3.accept()
print(1)
while True: 
    print(2)
    datas = client.recv(100)
    
    datas = datas.decode('utf-8')

    if datas[0] == "{":
        times = datetime.datetime.today()
        times = str(times)
        times = times[:19]
        datas = datas[:datas.find("[")+5] + datas[datas.find("]") :-2] + ", \"times\":" + times + "}\n"
        with open(path, 'a') as Temperature_file:
            Temperature_file.write(datas)