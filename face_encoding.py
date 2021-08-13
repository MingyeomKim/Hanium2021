import face_recognition
import cv2
import os
import numpy as np

encoding_file = open("photo/encoding.txt", 'w')
name_file = open('photo/name.txt', 'w')

dirname = "photo"
files = os.listdir(dirname)
for filename in files:
    name, ext = os.path.splitext(filename)
    if ext == ".jpg":
        pathname = os.path.join(dirname, filename)
        img = face_recognition.load_image_file(pathname)
        face_encoding = face_recognition.face_encodings(img)[0]
        for i in range(len(face_encoding)):
            encoding_file.write(str(face_encoding[i]))
            encoding_file.write(' ')
        encoding_file.write('\n')
        name_file.write(f'{name}\n')
