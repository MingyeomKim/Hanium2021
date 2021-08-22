from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect, secure_filename
from flask.helpers import url_for
import socket as sc
from encoding import face_encoding
from time import sleep
import json
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #파일 업로드 용량 제한 단위:바이트 #16MB 제한
app.secret_key = 'qwer1234'
path = 'C:\\Users\\Administrator\\Desktop\\final\\userList.json'

HOST = '0.0.0.0'
port = 1004


@app.route('/')
def loginPage():
    return render_template("loginPage.html")

@app.route('/mainPage', methods = ["GET"])
def mainPage():
    with open(path, 'r') as f:
        userList = json.load(f)

    if request.method == "GET":
        user_id = request.args.get("user_id")
        user_pw = request.args.get("user_pw")
        print(user_id, user_pw)
        if user_id == "":
            flash("아이디를 입력해주세요!")
            f.close()
            return redirect(url_for('loginPage'))
            
        elif user_pw == "":
            flash("비밀번호를 입력해주세요!")
            f.close()
            return redirect(url_for('loginPage')) 

        elif userList.get(user_id) != None:
            if userList[user_id][0] == user_pw:
                flash(f"{user_id}님 안녕하세요")
                f.close()
                return render_template("mainPage.html")
            else:
                flash("비밀번호 오류입니다!")
                f.close()
                return redirect(url_for('loginPage'))
                
        else:
            flash("아이디가 존재하지 않습니다!")
            f.close()
            return redirect(url_for('loginPage'))

# 문을 여는 함수
# -------------------------------------------
@app.route('/openDoor')
def opendoor():
    # commu.py에 문을 열라는 시그널 전송
    client.sendall('open'.encode())
    flash("문을 열었습니다.")
    return render_template("mainPage.html")
# -------------------------------------------


@app.route('/enterlogPage')
def enterlogPage():
    return render_template("enterlogPage.html")

@app.route('/signupPage')
def signupPage():
    return render_template("signupPage.html")

@app.route('/signupWaitPage', methods = ['GET'])
def signupWaitPage():
    with open(path, 'r') as f:
        userList = json.load(f)

    if request.method == "GET":
        new_id = request.args.get("new_id")
        new_pw = request.args.get("new_pw")
        new_email = request.args.get("new_email")

        print(new_id, new_pw, new_email)
        if new_id == "":
            flash("아이디를 입력해주세요!")
            f.close()
            return redirect(url_for('signupPage'))
        elif new_pw == "":
            flash("비밀번호를 입력해주세요!")
            f.close()
            return redirect(url_for('signupPage'))

        elif new_email == "":
            flash("이메일을 입력해주세요!")
            f.close()
            return redirect(url_for('signupPage'))

        elif userList.get(new_id) != None:
            flash("이미 존재하는 아이디입니다.")
            f.close()
            return redirect(url_for('signupPage'))
        else:
            print(json.dumps(userList, indent='\t'))
            userList[new_id] = [new_pw, new_email]
            with open(path, 'w') as outfile:
                json.dump(userList, outfile, indent='\t')
            
            with open(path, 'r') as f:
                new_userList = json.load(f)
            
            print(json.dumps(new_userList, indent='\t'))

            print("success")
            return render_template("loginPage.html")


@app.route('/userinfoPage')
def userinfoPage():
    return render_template('userinfoPage.html')

# 이미지를 json형식으로 넘겨주는 api
@app.route('/returnName')
def returnName():
    path = "../UserImage/"
    file_list = os.listdir(path)
    json = {}
    for i in range(len(file_list)):
        json[f'{i}'] = file_list[i]
    return json

# 삭제하려는 사진의 이름을 받아와서 서버내의 사진파일을 지우는 api
@app.route('/delete')
def delete():
    fileName = request.args.get('fileName')
    os.remove(f'../UserImage/{fileName}')

    # commu.py에 삭제한다는 시그널과 삭제할 이름 보내기
    # -------------------------------
    client.sendall('remove'.encode())
    r_name = fileName[:-4]
    client.sendall(r_name.encode())
    # -------------------------------
    return

@app.route('/fileUpload', methods=["POST"])
def fileUpload():
    if request.method == 'POST':
        img = request.files['file']
        uname = request.form.get('uname')
        img.save('C:\\Users\\Administrator\\Desktop\\UserImage\\' + secure_filename(f'{uname}.jpg'))

        # commu.py에 추가한다는 시그널과 추가할 이름, 인코딩한 데이터 전송
        # -------------------------------------------------------------------------------------------
        name = f'{uname}'
        client.sendall('add'.encode())
        client.sendall(name.encode());sleep(0.01)
        data = face_encoding('C:\\Users\\Administrator\\Desktop\\UserImage\\' + f'{uname}.jpg')
        client.sendall(data.encode())
        # -------------------------------------------------------------------------------------------
    return redirect('http://110.165.16.23:1219/userinfoPage')

if __name__ == "__main__":
    from waitress import serve

    # 소켓 열고 commu.py와 연결하고 client 주소 받기.
    # ----------------------------------------------------
    socket = sc.socket(sc.AF_INET, sc.SOCK_STREAM)
    socket.setsockopt(sc.SOL_SOCKET, sc.SO_REUSEADDR, 1)
    socket.bind((HOST, port))
    socket.listen()
    client, addr = socket.accept()
    # ----------------------------------------------------
    serve(app, host="0.0.0.0", port=1219)
    app.debug = True
    
    # app.run()