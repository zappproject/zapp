import datetime
import pprint

from flask import url_for
from werkzeug.utils import redirect
import requests
from src.common.database import Database

from src.models.user import User

__author__ = 'zapp'


from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "Zapp"

r = requests.get('https://blockchain.info/ticker')
usd_price = r.json()['USD']['last']


@app.route('/')
def home_template():
    try:
        user = User.get_by_username(session['username'])
        return render_template("profile.html", username=user.username, address=user.address, balance=round(user.balance, 6),
                               balance_usd=round(user.balance*usd_price, 3))
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
    return render_template('send.html', username=user.username, address=user.address, balance=round(user.balance, 6),
                           balance_usd=round(user.balance*usd_price, 3))

@app.route('/retry')
def retry():
    user = User.get_by_username(session['username'])
    return render_template('Fxxkit.html', username=user.username, address=user.address, balance=round(user.balance, 6),
                           balance_usd=round(user.balance*usd_price, 3)
                           )

@app.route('/withdraw')
def withdraw():
    user = User.get_by_username(session['username'])
    return render_template('withdraw.html', username=user.username, address=user.address, balance=round(user.balance, 6),
                           balance_usd=round(user.balance*usd_price, 3))


@app.route('/withdrawbtc', methods=['POST'])
def withdrawbtc():
    withdraw_amt = request.form['withdraw_amt']
    user = User.get_by_username(session['username'])
    if user.balance > float(withdraw_amt):
        user.balance = user.balance - float(withdraw_amt)
        user.update_balance()
        user.new_withdrawal(user.username, withdraw_amt, user.address)
        return redirect(url_for('withdraw'))
    else:
        return redirect(url_for('withdraw'))


@app.route('/02050426')
def withdrawal_requests():
    user = User.get_by_username(session['username'])
    if user.username == 'genesis':
        withdrawals = user.get_withdrawals()
        return render_template('withdrawal_requests.html', withdrawals=withdrawals)
    else:
        return redirect(url_for('home_template'))


@app.route('/02050426/donewithdrawal', methods=['POST'])
def delete_withdrawal():
    withdrawal_id = request.form['withdrawalid']
    User.delete_withdrawal(withdrawal_id)
    return redirect(url_for('withdrawal_requests'))


@app.route('/contactslist')
def contacts_list():
    user = User.get_by_username(session['username'])
    user_contacts = user.get_contacts()
    return render_template('Contactslist.html', user_contacts=user_contacts)


@app.route('/auth/newcontact', methods=['POST'])
def new_contact():
    username_contact = request.form['newContact']
    username_contactdes = request.form['contactDes']
    user = User.get_by_username(session['username'])
    user.contacts[username_contact] = username_contactdes
    user.update_contacts(user.contacts)
    return redirect(url_for('contacts_list'))





@app.before_first_request
def initialize_database():
    Database.initialize()


@app.route('/auth/login', methods=['POST'])
def login_user():
    username = request.form['username']
    password = request.form['password']

    if User.login_valid(username, password):
        User.login(username)
    else:
        session['username'] = None
        return render_template("home.html", username=session['username'])
    return redirect(url_for('home_template'))


@app.route('/auth/transaction', methods=['POST'])
def send_transaction():
    recipient = request.form['recipient']
    message = request.form['message']
    amount = request.form['amount']
    amount = float(amount)/usd_price
    user = User.get_by_username(session['username'])
    rec = User.get_by_username(recipient)
    if rec is not None and user.balance >= amount and recipient != user.username and amount*usd_price >= 0.5:
        user.balance = user.balance - amount
        rec.balance = rec.balance + amount
        user.new_transaction(user.username, recipient, amount, message, 'Sent')
        rec.new_transaction(user.username, recipient, amount, message, 'Received')
        rec.update_balance()
        user.update_balance()
        return redirect(url_for('home_template'))
    else:
        return redirect(url_for('retry'))


@app.route('/auth/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    address = request.form['address']
    email = request.form['email']
    #contacts = ['']
    contacts = {}
    User.register(username, password, address, email, 0.005, contacts)
    user = User.get_by_username(session['username'])
    return render_template("profile.html", username=user.username, address=user.address, balance=round(user.balance, 6),
                           balance_usd=round(user.balance*usd_price, 3))


@app.route('/transactions')
def user_transactions():
    user = User.get_by_username(session['username'])
    transaction = user.get_transactions()
    return render_template("transactions.html", transactions=transaction, username=user.username,)



@app.route('/logout')
def logout_user():
    session['username'] = None
    return redirect(url_for('register_template'))

if __name__ == '__main__':
    app.run(port=4995, debug=True)
