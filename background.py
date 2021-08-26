import os
import serial
import pyfirmata
from socket import *
import camera
from time import sleep
import numpy as np
from importlib import reload

serial_port = '/dev/ttyACM0'
board = pyfirmata.Arduino('/dev/ttyACM0')

# set baud rate
baud_rate = 9600

# serial, pin open
ser = serial.Serial(serial_port, baud_rate)
pin3 = board.get_pin('d:3:o')

pid = os.fork()

if pid == 0:
    HOST2 = '110.165.16.23'
    PORT2 = 31005
    client_socket2 = socket(AF_INET, SOCK_STREAM)
    client_socket2.connect((HOST2, PORT2))
    # arduino port

    
    # discard trash value
    # ser.readline()
  
    
    # json file
#     write_to_file_path = "/home/pi/readTemperature/Temperature.json";
#     output_file = open(write_to_file_path,"w");
    
    while True:
        print('ready')
        # wait signal from arduino
        line = ser.readline()
        line = line.decode("UTF-8")
        line = line.strip()
        temperature = line[16:21]
        print(temperature)
        
        # fork process
        ppid = os.fork()
        # import new file
        reload(camera)
        
        # if child process
        if ppid == 0:
            # recieve Success or Fail and name from camera module
            signal, name = camera.face(temperature)
            
            # if success
            if(signal == 1):
                
                line = line[:-1] + f', "name":"{name}"' + line[-1] + "\n"
                
                # open door
                pin3.write(1)
                sleep(1)
                pin3.write(0)
                
                # record data
                # output_file.write(line)
                
                # send Temperature.json
                print('send Temperature information to server')
                print(line.encode("UTF-8"))
                # solve codec error 
                client_socket2.send(line.encode("UTF-8"))
            
            else:
                print('Time Over. Please retry')
                
            exit(0)
            
        # if parent process
        else:
            # wait for child process's die
            os.wait()
            sleep(3)

else:
    # socket open and connect to server
    HOST = '110.165.16.23'
    PORT = 31004
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    
    while True:
        # wait and recieve signal
        sig = client_socket.recv(8)
        
        # if recieve add signal
        if sig.decode('utf-8') == 'add':
            # recieve name and data
            name = client_socket.recv(64)
            name = name.decode('utf-8')
            
            data = client_socket.recv(2048)
            data = data.decode('utf-8')
            
            data_2 = client_socket.recv(2048)
            data_2 = data_2.decode('utf-8')
            
            # file open
            file = open('./photo/encoding.txt', 'a')
            file_1 = open('./photo/name.txt', 'a')
            
            # data save
            file.write(data + data_2 + '\n')
            file_1.write(name + '\n')

            # file close
            file.close()
            file_1.close()
        
        # if recieve open signal
        elif sig.decode('utf-8') == 'open':
            # send open signal to arduino
            pin3.write(1)
            sleep(1)
            pin3.write(0)
        
        # if recieve remove signal
        else:
            # recieve name from server and decode
            name = client_socket.recv(64)
            name = name.decode('utf-8')
            
            # open file to read data
            f = open('./photo/name.txt', 'r')
            f_1 = open('./photo/encoding.txt', 'r')
            
            # recieve data and process
            names = f.readlines()
            encodes = f_1.readlines()
            
            # remove \n
            for i in range(len(names)):
                names[i] = names[i].strip()
                encodes[i] = encodes[i].strip()
            
            # find the index of the name to be deleted
            ind = names.index(name)
            
            # file close
            f.close()
            f_1.close()
            
            # file open to write data
            f = open('./photo/name.txt', 'w')
            f_1 = open('./photo/encoding.txt', 'w')
            
            # fill file except name to be deleted
            for i in range(len(names)):
                if i != ind:
                    f.write(names[i])
                    f.write('\n')
                    f_1.write(encodes[i])
                    f_1.write('\n')
                    
            # file close
            f.close()
            f_1.close()