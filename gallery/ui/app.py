from flask import Flask, request, render_template, jsonify, redirect, url_for, session, flash
#import db_functions
from functools import wraps
from werkzeug.utils import secure_filename

from gallery.tools import db_functions
from gallery.tools.secrets import get_secret_flask_session

import os

app = Flask(__name__)
app.secret_key = get_secret_flask_session()

db_connect = db_functions.connect()
s3_connect = db_functions.s3_connect()

def check_admin():
    return 'username' in session and session['username'] == 'admin'

def check_user():
    return 'username' in session

# def requires_admin(view):
#     @wraps(view)
#     def decorated(**kwargs):
#         if not check_admin():
#             return render_template('denied.html')
#         view(**kwargs)
#     return decorated

# def requires_user(view):
#     @wraps(view)
#     def decorated(**kwargs):
#         if not check_user():
#             return render_template('denied.html')
#         view(**kwargs)
#     return decorated

@app.route('/')
def reroute():
    return redirect('/login')

@app.route('/admin')
def index():
    if check_admin():
        db_connect
        users = db_functions.list_users()
        #return jsonify({'user_data': users})
        return render_template('admin.html', users=users)
    else:
        return render_template('denied.html')

@app.route('/admin/edit/<user>', methods=('GET', 'POST'))
def edit(user):
    db_connect
    userinfo = db_functions.list_user(user)

    if request.method == 'POST':
        username = userinfo[0]
        password = request.form['password']
        fullname = request.form['fullname']

        db_connect
        db_functions.edit_user(username, password, fullname)
        return redirect('/')

    return render_template('edituser.html', userinfo=userinfo)

@app.route('/admin/adduser/', methods=('GET', 'POST'))
def add():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']

        db_connect
        db_functions.add_user(username, password, fullname)
        return redirect('/')

    return render_template('adduser.html')

@app.route('/admin/delete/<user>')
def delete(user):
    db_connect
    db_functions.delete_user(user)
    return redirect('/')

@app.route('/home')
def home():
    if check_admin() or check_user():
        return render_template('home.html')
    else:
        return render_template('denied.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_connect
        user = db_functions.login(username, password)
        if user is None or user[1] != password:
            error = 'Invalid credentials!'
        else:
            session['username'] = username
            return redirect("/home")
    return render_template('login.html', error=error)

@app.route('/invalidLogin')
def invalidLogin():
    return "invalid credentials"

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        username = session.get("username")
        file = request.files['user_file']
        db_functions.upload_file_to_s3(file, "edu.au.cc.img-gallery", username)
        return redirect("/home")
    return render_template('upload.html')

@app.route('/view', methods=['GET'])
def view():
        username = session.get("username")
        imgs = db_functions.get_files_from_s3("edu.au.cc.img-gallery", username)
        return render_template('view.html', imgs=imgs)

