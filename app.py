from flask import Flask, render_template, request, session, flash, redirect
from sqlite3 import Connection
from werkzeug.security import generate_password_hash

from config import secret, db_file
from query import query
import user
import comments
from posts import Posts
from profile import Profile


app = Flask(__name__)
app.secret_key = secret

conn = Connection(db_file)
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

    if not user.validate(username, password):
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
    password = request.form['password']
    password_again = request.form['password-again']

    if username == '' or password == '' or password_again == '':
        flash('Fields cannot be empty!')
        
    elif user.exists(username):
        flash('Username has been taken.')

    elif password != password_again:
        flash('The passwords you have given don\'t match.')

    else:
        user.create(username, generate_password_hash(password))
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
        return render_template('post-form.html', post=None)
    return 'Forbidden'

@app.route('/create-new-post', methods=['POST', 'GET'])
def create_new_post():
    id = query().select('id').from_('Users').where('username = ?').execute(session['username']).fetchone()[0]
    posts.new(id,
              request.form['title'],
              request.form['context'],
              request.form['content'])
    flash('New Post Added!')
    return redirect('/')

@app.route('/edit-post-form/<int:post_id>', methods=['GET'])
def edit_post_form(post_id):
    post = posts.by_id(post_id)
    if post.username != session['username']:
        return 'Forbidden'
    
    # Delete the old post
    return render_template('post-form.html', post=post)
    
@app.route('/edit-post/<int:post_id>', methods=['POST'])
def edit(post_id):
    post = posts.by_id(post_id)
    if post.username != session['username']:
        return 'Forbidden'
    posts.update(post.id,
                 request.form['title'],
                 request.form['context'],
                 request.form['content'])

    flash('Update successful!')
    return redirect(f'/post/{post_id}')

@app.route('/post/<int:post_id>')
def show_post(post_id):
    post = posts.by_id(post_id)
    comment_list = comments.get_post_comments(post_id)
    print(post.content)
    return render_template('post.html', post=post, comments=comment_list)

@app.route('/search')
def search():
    query = request.args.get('query')
    results = posts.search(query)
    if not results:
        results = []
    print(results)
    return render_template('search-results.html', query=query, post_previews=results)

@app.route('/delete/<int:post_id>')
def delete(post_id):
    post = posts.by_id(post_id)
    if post.username != session['username']:
        return 'Forbidden'
    
    query().delete('').from_('Posts').where('id = ?').execute(post.id)
    flash('Post deleted!')
    return redirect('/')

@app.route('/profile/<string:username>')
def profile_page(username):
    if not user.exists(username):
        return f'User {username} doesn\'t exist.'

    user_id, join_date = query().select('id, ts')      \
                                .from_('Users')        \
                                .where('username = ?') \
                                .execute(username)     \
                                .fetchone()
    
    posts_ = posts.by_user(user_id)
    post_count = len(posts_)
    join_date = join_date[:10]
    
    return render_template('profile.html',
                           profile=Profile(username,
                                           post_count,
                                           join_date=join_date),
                           post_previews=posts_)

