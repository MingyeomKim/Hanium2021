from flask import Flask, render_template, request
from werkzeug.utils import redirect, secure_filename
import os
app = Flask(__name__)

@app.route('/')
def loginPage():
    return render_template("loginPage.html")

@app.route('/printinfo', methods = ["GET"])
def printinfo():
    if request.method == 'GET':
        user = request.args.to_dict()

@app.route('/mainPage')
def mainPage():
    if request.method == 'GET':
        user = request.args.to_dict()
    return render_template("mainPage.html")

@app.route('/enterlogPage')
def enterlogPage():
    return render_template("enterlogPage.html")

@app.route('/signupPage')
def signupPage():
    return render_template("signupPage.html")

@app.route('/userinfoPage')
def userinfoPage():
    return render_template('userinfoPage.html')

@app.route('/form', methods=["POST"])
def form():
    if request.method == 'POST':
        img = request.files['file']
        uname = request.form.get('uname')
        img.save('C:\\Users\\Administrator\\Desktop\\UserImage\\' + secure_filename(f'{uname}.jpg'))
        pid = os.fork()
        if pid != 0:
            argv = ('')
            os.execv
    return redirect('http://110.165.16.23:1219/userinfoPage')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=1219)
    app.debug = True
    app.run()