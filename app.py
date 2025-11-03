from flask import Flask

from db import DB

app = Flask(__name__)
db = DB('database.db')

@app.route('/')
def index():
  return 'Hello World!'


