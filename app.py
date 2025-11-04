from flask import Flask, render_template, request, session, flash
from werkzeug.security import check_password_hash

from config import db_file, secret
from db import DB

app = Flask(__name__)
app.secret_key = secret

db = DB(db_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login-form')
def login_form():
    return render_template('login-form.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    password_hash = db.execute("""SELECT password_hash
                                  FROM Users
                                  WHERE username = ?""", [username])
    if not password_hash or not check_password_hash(password_hash, password):
        flash('Incorrect username or password.')
    else:
        flash('Login successful!')
        session['username'] = username
    
    return render_template('login-form.html')


