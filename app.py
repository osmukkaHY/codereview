from flask import Flask, render_template

from db import DB

app = Flask(__name__)
db = DB('database.db')

@app.route('/')
def index():
    return render_template('index.html')


