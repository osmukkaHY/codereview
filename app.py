from flask import Flask, render_template, request, session, flash, redirect
from sqlite3 import Connection
from werkzeug.security import generate_password_hash

from config import secret, db_file
from query import query
from users import Users
from posts import Posts


app = Flask(__name__)
app.secret_key = secret

conn = Connection(db_file)
users = Users()
posts = Posts()


@app.route('/')
def index():
    post_previews = posts.n_recent(5)
    return render_template('index.html', post_previews=post_previews)


@app.route('/login-form', methods=['GET'])
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
    
    return redirect('/')


@app.route('/signup-form', methods=['GET'])
def signup_form():
    return render_template('signup-form.html')


@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    if users.exists(username):
        flash('Username has been taken.')
        return render_template('signup-form.html')

    password = request.form['password']
    password_again = request.form['password-again']
    if password != password_again:
        flash('The passwords you have given don\'t match.')
        return render_template('signup_form.html')

    users.add(username, generate_password_hash(password))
    flash('User successfully created!')
    return render_template('signup-form.html')


@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
    return render_template('index.html')

@app.route('/new-post-form')
def new_post_form():
    if session['username']:
        return render_template('new-post-form.html', post=None)
    return 'Forbidden'

@app.route('/create-new-post', methods=['POST', 'GET'])
def create_new_post():
    posts.new(session['username'],
              request.form['title'],
              request.form['context'],
              request.form['content'])
    flash('New Post Added!')
    return redirect('/')

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = posts.by_id(post_id)
    print(post.content)
    return render_template('post.html', post=post)

@app.route('/search')
def search():
    query = request.args.get('query')
    results = posts.search(query)
    if not results:
        results = []
    print(results)
    return render_template('search-results.html', query=query, posts=results)

@app.route('/edit/<int:post_id>')
def edit(post_id):
    post = posts.by_id(post_id)
    if post.username != session['username']:
        return 'Forbidden'
    
    # Delete the old post
    query().delete('').from_('Posts').where('id = ?').execute(post.id)
    return render_template('new-post-form.html', post=post)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    post = posts.by_id(post_id)
    if post.username != session['username']:
        return 'Forbidden'
    
    query().delete('').from_('Posts').where('id = ?').execute(post.id)
    flash('Post deleted!')
    return redirect('/')

