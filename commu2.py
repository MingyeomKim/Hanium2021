import socket as sc

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
    temperature_data = client.recv(100)
    print(3)
    temperature_data = temperature_data.decode('utf-8')
    print(4)
    print(temperature_data)
    with open(path, 'a') as Temperature_file:
        Temperature_file.write(temperature_data)