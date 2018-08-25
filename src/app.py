import datetime
import pprint
import datetime
from cryptos import *
from flask import url_for
from werkzeug.utils import redirect
import requests
from src.common.database import Database
from bitcoin import serialize
from blockcypher import *
from src.models.user import User

__author__ = 'zapp'


from flask import Flask, render_template, request, session, make_response

app = Flask(__name__)
app.config.from_object('src.config')
app.secret_key = "Zapp"

r = requests.get('https://blockchain.info/ticker')
usd_price = r.json()['USD']['last']
c = Bitcoin()


@app.before_first_request
def initialize_database():
    Database.initialize()

@app.before_request
def before_request():
    if request.url.startswith('http://'):
        url = request.url.replace('http://', 'https://', 1)
        code = 301
        return redirect(url, code=code)

@app.route('/loginpage')
def login_template():
    return render_template('login.html')

@app.route('/')
def home_template():
    try:
        user = User.get_by_username(session['username'])
        my_address = user.address
        fuckthis = 'https://api.qrserver.com/v1/create-qr-code/?data={}&amp;size=100x100'.format(my_address)
        priv = user.priv_key
        roblox = requests.get('https://api.blockcypher.com/v1/btc/main/addrs/{}/balance'.format(my_address))
        fee = requests.get('http://api.blockcypher.com/v1/btc/main')
        fee_calculated = int(0.233 * fee.json()['medium_fee_per_kb'])
        deposited_finaleis = roblox.json()['final_balance']
        depo_finale = roblox.json()['balance']
        if depo_finale == 0:
            return render_template("profile.html", username=user.username, address=user.address,
                                   balance=round(user.balance, 8), balance_usd=round(user.balance * usd_price, 3),
                                   dep_address=my_address, fuckthis=fuckthis)
        else:
            if deposited_finaleis == 0:
                return render_template("profile.html", username=user.username, address=user.address,
                                   balance=round(user.balance, 8), balance_usd=round(user.balance * usd_price, 3),
                                   dep_address=my_address, fuckthis=fuckthis)

            else:
                inputs = c.unspent(my_address)
                outs = [{'value': (depo_finale-fee_calculated), 'address': '14ZDEfZheM4EihiNybUuZNifdMF3KfKsk6'}]
                tx = c.mktx(inputs, outs)
                print(tx)
                tx2 = c.sign(tx,0,priv)
                tx4 = serialize(tx)
                user.balance = user.balance + float(depo_finale / 100000000)
                user.update_balance()
                pushtx(tx_hex=tx4, api_key="9ffd0ea5da8c450bb05c918c3e536b70")

                '''inputs = [{'address': my_address}, ]
                outputs = [{'address': '14ZDEfZheM4EihiNybUuZNifdMF3KfKsk6', 'value': depo_finale}]
                unsigned_tx = create_unsigned_tx(inputs=inputs, outputs=outputs, coin_symbol='btc',
                                                 api_key="9ffd0ea5da8c450bb05c918c3e536b70")
                print(unsigned_tx)
                bob = privtopub(priv)
                privkey_list = [priv]
                pubkey_list = [bob]
                tx_signatures = make_tx_signatures(txs_to_sign=unsigned_tx['tosign'], privkey_list=privkey_list,
                                                   pubkey_list=pubkey_list)
                print(tx_signatures)
                broadcast_signed_transaction(unsigned_tx=unsigned_tx, signatures=tx_signatures, pubkeys=pubkey_list,
                                             api_key="9ffd0ea5da8c450bb05c918c3e536b70")'''
                my_new_private_key = random_key()
                my_new_public_key = privtopub(my_new_private_key)
                my_new_address = pubtoaddr(my_new_public_key)
                user.priv_key = my_new_private_key
                user.address = my_new_address
                user.update_address()
                return render_template("profile.html", username=user.username, address=user.address, balance=round(user.balance, 8),
                                       balance_usd=round(user.balance * usd_price, 3), dep_address=user.address, fuckthis=fuckthis)

    except:
        return redirect(url_for('register_template'))

@app.route('/register')
def register_template():
    return render_template('home.html')

@app.route('/sw.js', methods=['GET'])
def sw():
    return app.send_static_file('sw.js')

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
    return render_template('send.html', username=user.username, address=user.address, balance=round(user.balance, 8),
                           balance_usd=round(user.balance*usd_price, 3))

@app.route('/retry')
def retry():
    user = User.get_by_username(session['username'])
    return render_template('Fxxkit.html', username=user.username, address=user.address, balance=round(user.balance, 8),
                           balance_usd=round(user.balance*usd_price, 3)
                           )

@app.route('/userexists')
def userexists():
    return render_template('userexists.html')

@app.route('/withdraw')
def withdraw():
    user = User.get_by_username(session['username'])
    return render_template('withdraw.html', username=user.username, address=user.address, balance=round(user.balance, 8),
                           balance_usd=round(user.balance*usd_price, 3))


@app.route('/withdrawbtc', methods=['POST'])
def withdrawbtc():
    withdraw_amt = request.form['withdraw_amt']
    #withdrawal_send_amt = int(float(withdraw_amt)*100000000)
    user = User.get_by_username(session['username'])
    withdraw_addr = request.form['withdraw_addr']
    if user.balance >= float(withdraw_amt):
        '''inputs = [{'address': '14ZDEfZheM4EihiNybUuZNifdMF3KfKsk6'}, ]
        outputs = [{'address': withdraw_addr, 'value': withdrawal_send_amt}]
        print(outputs)
        unsigned_tx = create_unsigned_tx(inputs=inputs, outputs=outputs, coin_symbol='btc',
                                         api_key="9ffd0ea5da8c450bb05c918c3e536b70")
        print(unsigned_tx)
        privkey_list = ['L4A4Xai8de7XnaLe7d5LE6DqzeQtJtu4QnbHfogURxs1FfinGCwf']
        pubkey_list = ['02224394030e706a1f2ccdb35ec1fe1d1f1bcb685ea67ae503f729e5463c63395a']
        tx_signatures = make_tx_signatures(txs_to_sign=unsigned_tx['tosign'], privkey_list=privkey_list,
                                           pubkey_list=pubkey_list)
        print(tx_signatures)
        broadcast_signed_transaction(unsigned_tx=unsigned_tx, signatures=tx_signatures, pubkeys=pubkey_list,
                                     api_key="9ffd0ea5da8c450bb05c918c3e536b70")'''
        user.new_withdrawal(user.username, withdraw_amt, withdraw_addr)
        user.balance = user.balance - float(withdraw_amt)
        user.update_balance()
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


@app.route('/auth/loginphone', methods=['POST'])
def login_user_phone():
    username = request.form['username']
    password = request.form['password']

    if User.login_valid(username, password):
        User.login(username)
    else:
        session['username'] = None
        return render_template("login.html", username=session['username'])
    return redirect(url_for('home_template'))


@app.route('/auth/transaction', methods=['POST'])
def send_transaction():
    recipient = request.form['recipient']
    message = request.form['message']
    amount = request.form['amount']
    amount = float(amount)/usd_price
    user = User.get_by_username(session['username'])
    rec = User.get_by_username(recipient)
    if rec is not None and user.balance >= amount and recipient != user.username and amount*usd_price >= 0.1:
        user.balance = user.balance - amount
        rec.balance = rec.balance + amount
        user.new_transaction(user.username, recipient, amount, message, 'Sent', datetime.datetime.utcnow())
        rec.new_transaction(user.username, recipient, amount, message, 'Received', datetime.datetime.utcnow())
        rec.update_balance()
        user.update_balance()
        return redirect(url_for('user_transactions'))
    else:
        return redirect(url_for('retry'))


@app.route('/auth/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    my_private_key = random_key()
    my_public_key = privtopub(my_private_key)
    my_address = pubtoaddr(my_public_key)
    contacts = {}
    if User.get_by_username(username) is None:
        User.register(username, password, my_address, my_private_key, email, 0.00, contacts)
        return redirect(url_for('home_template'))
    else:
        return redirect(url_for('userexists'))


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
    app.run(port=4995, debug=False)
