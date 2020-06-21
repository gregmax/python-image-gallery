from flask import Flask, request, render_template, jsonify, redirect, url_for
#import db_functions
from gallery.ui import db_functions

app = Flask(__name__)

@app.route('/')
def reroute():
    return redirect('/admin')

@app.route('/admin')
def index():
    db_functions.connect()
    users = db_functions.list_users()
    #return jsonify({'user_data': users})
    return render_template('admin.html', users=users)

@app.route('/admin/edit/<user>', methods=('GET', 'POST'))
def edit(user):
    db_functions.connect()
    userinfo = db_functions.list_user(user)

    if request.method == 'POST':
        username = userinfo[0]
        password = request.form['password']
        fullname = request.form['fullname']

        db_functions.connect()
        db_functions.edit_user(username, password, fullname)
        return redirect('/')
    
    return render_template('edituser.html', userinfo=userinfo)

@app.route('/admin/adduser/', methods=('GET', 'POST'))
def add():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']

        db_functions.connect()
        db_functions.add_user(username, password, fullname)
        return redirect('/')
    
    return render_template('adduser.html')

@app.route('/admin/delete/<user>')
def delete(user):
    db_functions.connect()
    db_functions.delete_user(user)
    return redirect('/')
