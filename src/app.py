from flask import url_for
from werkzeug.utils import redirect

from src.common.database import Database

from src.models.user import User

__author__ = 'zapp'


from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "Zapp"


@app.route('/')
def home_template():
    try:
        user = User.get_by_username(session['username'])
        return render_template("profile.html", username=user.username, address=user.address, balance=user.balance)
    except:
        return render_template('home.html')

@app.route('/register')
def register_template():
    return render_template('home.html')


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
    user = User.get_by_username(session['username'])
    return render_template('send.html', username=user.username, address=user.address, balance=user.balance)

@app.route('/withdraw')
def withdraw():
    user = User.get_by_username(session['username'])
    return render_template('withdraw.html', username=user.username, address=user.address, balance=user.balance)







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
    return render_template("profile.html", username=session['username'], address=user.address, balance=user.balance)

@app.route('/auth/transaction', methods=['POST'])
def send_transaction():
    recipient = request.form['recipient']
    message = request.form['message']
    amount = request.form['amount']
    amount = float(amount)

    user = User.get_by_username(session['username'])
    rec = User.get_by_username(recipient)

    user.balance = round(float(user.balance) - amount, 2)
    rec.balance = round(float(rec.balance) + amount, 2)

    user.new_transaction(recipient, amount, message, 'sent')
    rec.new_transaction(recipient, amount, message, 'received')
    rec.update_balance()
    user.update_balance()
    return redirect(url_for('home_template'))


@app.route('/auth/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    address = request.form['address']
    User.register(username, password, address, 5)
    user = User.get_by_username(session['username'])
    return render_template("profile.html", username=user.username, address=user.address, balance=user.balance)

@app.route('/transactions')
def user_blogs():
    user = User.get_by_username(session['username'])
    transactions = user.get_transactions(user.username)
    return render_template("transactions.html", transactions=transactions)



@app.route('/logout')
def logout_user():
    session['username'] = None
    return redirect(url_for('register_template'))

if __name__ == '__main__':
    app.run(port=4995, debug=True)
