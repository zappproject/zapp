from flask import url_for
from werkzeug.utils import redirect

from src.common.database import Database
from src.models.blog import Blog
from src.models.post import Post
from src.models.user import User

__author__ = 'zapp'


from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)  # '__main__'
app.secret_key = "zapp"


@app.route('/')
def home_template():
    try:
        user = User.get_by_username(session['username'])
        return render_template("profile.html", username=user.username, address=user.address)
    except:
        return render_template('home.html')

@app.route('/register')
def register_template():
    return render_template('home.html')

@app.route('/login')
def login_template():
    return render_template('login.html')



@app.route('/contribute')
def contribute():
     return render_template('Contribute.html')

@app.route('/aboutus')
def about():
     return render_template('aboutus.html')

@app.route('/FAQ')
def FAQ():
    return render_template('faq.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/send')
def send():
    return render_template('send.html')

@app.route('/withdraw')
def withdraw():
    return render_template('withdraw.html')







@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    if User.login_valid(username, password):
        User.login(username)
        user = User.get_by_username(session['username'])
    else:
        session['username'] = None
        return render_template("home.html", username=session['username'])
    return render_template("profile.html", username=session['username'], address=user.address)


@app.route('/auth/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    address = request.form['address']
    User.register(username, password, address)
    user = User.get_by_username(session['username'])
    return render_template("profile.html", username=user.username, address=user.address)


@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_username(session['username'])

    blogs = user.get_blogs()

    return render_template("user_blogs.html", blogs=blogs, username=user.username)


@app.route('/blogs/new', methods=['POST', 'GET'])
def create_new_blog():
    if request.method == 'GET':
        return render_template('new_blog.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_username(session['username'])

        new_blog = Blog(user.username, title, description, user._id)
        new_blog.save_to_mongo()

        return make_response(user_blogs(user._id))


@app.route('/posts/<string:blog_id>')
def blog_posts3(blog_id):
    blog = Blog.from_mongo(blog_id)
    posts = blog.get_posts()
    return render_template('posts.html', posts=posts, blog_title=blog.title, blog_id=blog._id)

@app.route('/posts/new/<string:blog_id>', methods=['POST', 'GET'])
def create_new_post(blog_id):
    if request.method == 'GET':
        return render_template('new_post.html', blog_id=blog_id)
    else:
        title = request.form['title']
        content = request.form['content']
        user = User.get_by_username(session['username'])

        new_post = Post(blog_id, title, content, user.username)
        new_post.save_to_mongo()

        return make_response(blog_posts(blog_id))

@app.route('/logout')
def logout_user():
    session['username'] = None
    return redirect(url_for('register_template'))

if __name__ == '__main__':
    app.run(port=4995, debug=True)
