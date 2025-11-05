from flask import Flask, render_template, request, session, flash
from werkzeug.security import generate_password_hash

from config import secret
from db import DB
from users import Users

app = Flask(__name__)
app.secret_key = secret

db = DB()
users = Users()

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

    if not users.validate(username, password):
        flash('Incorrect username or password.')
    else:
        flash('Login successful!')
        session['username'] = username
    
    return render_template('login-form.html')

@app.route('/signup-form')
def signup_form():
    return render_template('signup-form.html')

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    print(type(username))
    password = request.form['password']
    password_again = request.form['password-again']

    if password != password_again:
        flash('The passwords you have given don\'t match.')
        return render_template('signup_form.html')

    password_hash = generate_password_hash(password)
    if len(db.fetch("""SELECT * FROM Users WHERE username = ?""", username)):
        flash('Username has been taken.')
        return render_template('signup-form.html')

    db.fetch('INSERT INTO Users (username, password_hash) VALUES (?, ?)',
               username, password_hash)
    flash('User successfully created!')
    return render_template('signup-form.html')


