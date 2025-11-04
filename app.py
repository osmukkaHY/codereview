from flask import Flask, render_template

from config import db_file
from db import DB

app = Flask(__name__)
db = DB(db_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login-form')
def login_form():
    return render_template('login-form.html')
