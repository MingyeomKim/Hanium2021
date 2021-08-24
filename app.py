from flask import Flask, render_template, request, flash
from werkzeug.utils import redirect, secure_filename
from flask.helpers import url_for
import socket as sc
from encoding import face_encoding
from time import sleep
import json
import os
from PIL import Image

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #파일 업로드 16MB용량 제한
app.secret_key = 'qwer1234' #소켓 통신을 위한 Key 설정

path = 'C:\\Users\\Administrator\\Desktop\\final\\userList.json'
 #사용자 정보를 저장한 userList.json 파일의 경로를 변수화
HOST = '0.0.0.0'
port = 1004
#서버에서 클라이언트로 데이터 전송을 하기 위한 HOST와 PORT 지정

#  기본 Url에 접근할 때 로그인 화면으로 이동
@app.route('/')
def loginPage():
    return render_template("loginPage.html")

# mainPage로 이동
@app.route('/mainPage', methods = ["GET"])
def mainPage():
    with open(path, 'r') as f:
        userList = json.load(f) 
        #userList.json 파일을 'f'라는 이름으로 열어서 변수에 저장

    if request.method == "GET":
        user_id = request.args.get("user_id")
        user_pw = request.args.get("user_pw")
        # GET방식으로 user_id, user_pw 값을 받음
        print(user_id, user_pw)
        #user_id를 입력하지 않은 경우
        if user_id == "":
            flash("아이디를 입력해주세요!")
            f.close()
            return redirect(url_for('loginPage'))
        # user_pw를 입력하지 않은 경우
        elif user_pw == "":
            flash("비밀번호를 입력해주세요!")
            f.close()
            return redirect(url_for('loginPage')) 
        # 입력한 user_id에 해당하는 key가 존재할 경우 
        elif userList.get(user_id) != None:
            if userList[user_id][0] == user_pw: #비밀번호가 일치하면
                flash(f"{user_id}님 안녕하세요")
                f.close()
                return render_template("mainPage.html")
                #로그인 된 페이지로 이동
            else:
                flash("비밀번호 오류입니다!")
                f.close()
                return redirect(url_for('loginPage'))
        # 입력한 정보가 일치하지 않는 경우
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


# 출입 로그를 띄우는 화면
@app.route('/enterlogPage')
def enterlogPage():
    return render_template("enterlogPage.html")
    
# 회원가입 화면 
@app.route('/signupPage')
def signupPage():
    return render_template("signupPage.html")


@app.route('/signupWaitPage', methods = ['GET'])
def signupWaitPage():
    # userList.json 파일을 'f'라는 이름으로 불러옴
    with open(path, 'r') as f:
        userList = json.load(f)

    # GET 메소드로 사용자의 id, pw, email을 각각 변수에 담음 
    if request.method == "GET":
        new_id = request.args.get("new_id")
        new_pw = request.args.get("new_pw")
        new_email = request.args.get("new_email")
               # id가 비어있는 경우 
        if new_id == "":
            flash("아이디를 입력해주세요!")
            f.close()
            return redirect(url_for('signupPage'))
        # pw가 비어있는 경우 
        elif new_pw == "":
            flash("비밀번호를 입력해주세요!")
            f.close()
            return redirect(url_for('signupPage'))
        # email이 비어있는 경우 
        elif new_email == "":
            flash("이메일을 입력해주세요!")
            f.close()
            return redirect(url_for('signupPage'))
        # userList의 key에서 입력한 id가 이미 존재하는 경우 
        elif userList.get(new_id) != None:
            flash("이미 존재하는 아이디입니다.")
            f.close()
            return redirect(url_for('signupPage'))
        # 회원가입을 정상적으로 진행한 경우 
        else:
            userList[new_id] = [new_pw, new_email]
            # 새로운 key와 value를 추가
            with open(path, 'w') as outfile:
                json.dump(userList, outfile, indent='\t')
            # 'outfile'이라는 이름으로 userList.json 파일을 쓰기모드로 연다.
            with open(path, 'r') as f:
                new_userList = json.load(f)
                # 읽기 모드로 새로운 userList.json 파일을 열고 

            return render_template("loginPage.html")

# 사용자 정보를 출력하는 화면
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

# 파일 업로드 메소드 추가
@app.route('/fileUpload', methods=["POST"])
def fileUpload():
    if request.method == 'POST':
        img = request.files['file'] # POST 방식으로 넘겨받은 file 가져오기 
        uname = request.form.get('uname') # POST 방식으로 넘겨받은 uname(사용자 이름) 가져오기
        img.save('C:\\Users\\Administrator\\Desktop\\UserImage\\' + secure_filename(f'{uname}.jpg'))
        # commu.py에 추가한다는 시그널과 추가할 이름, 인코딩한 데이터 전송
        # -------------------------------------------------------------------------------------------
        name = f'{uname}'
        image = Image.open(f'C:\\Users\\Administrator\\Desktop\\UserImage\\{uname}.jpg')
        image_resize = image.resize((1000,1000))
        image_resize = image_resize.transpose(Image.ROTATE_90)
        image_resize.save(f'C:\\Users\\Administrator\\Desktop\\UserImage\\{uname}.jpg')
        # image = Image.open(f'C:\\Users\\Administrator\\Desktop\\UserImage\\{uname}.jpg')
        # buffer = StringIO()
        # image.save(buffer,'jpeg',quality=100)
        # buffer.seek(0)
        # with open(f'C:\\Users\\Administrator\\Desktop\\UserImage\\{uname}.jpg','wb') as nfile:
        #     nfile.write(buffer.getvalue())
        # print('실행됨')
        client.sendall('add'.encode())
        client.sendall(name.encode());sleep(0.01)
        data = face_encoding('C:\\Users\\Administrator\\Desktop\\UserImage\\' + f'{uname}.jpg')

        client.send(data.encode())
        # -------------------------------------------------------------------------------------------
    return redirect('http://110.165.16.23:1219/userinfoPage')

@app.route('/enterLog', methods=["GET"])
def returnEnterLog():
    f = open('./Temperature.txt','r')
    lines = f.readlines()
    returnjson = {}
    count = 0
    for line in lines:
        returnjson[f'{count}'] = line
        count += 1
    
    return returnjson

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
    app.jinja_env.auto_reload = True
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.debug = True

    # app.run()