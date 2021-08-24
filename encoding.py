import face_recognition as fr

def face_encoding(route: str) -> str:
    img = fr.load_image_file(route)
    print(fr.face_encodings(img))
    print(type(fr.face_encodings(img)))
    encode = fr.face_encodings(img)[0]
    encode = map(str, encode)
    return ' '.join(encode)