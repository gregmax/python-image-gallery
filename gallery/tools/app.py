from flask import Flask
from flask import request
from flask import render_template
import db_functions

app = Flask(__name__)

@app.route('/')
def admin():
    return render_template('admin.html')

@app.route('/admin/listUsers')
def goodbye():
    return 'Goodbye!'

@app.route('/admin/addUser')
def greet():
    return 'Nice to meet you,'

@app.route('/admin/editUser')
def test():
    return 'test'
