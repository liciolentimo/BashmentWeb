from flask import Flask, render_template, url_for, jsonify, request, session
import stripe
from config import Config
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import *
import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config.from_object(Config)
DB_URI = app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(DB_URI)
metadata = MetaData(engine)
session = Session(engine)
Base = automap_base()
Base.prepare(engine, reflect=True)
Accounts = Base.classes.bashmenttbl



app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_mWaJhKb35BpMP15bfsE1CB9j00aBE0OgQT'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51EkSfRDE2fV8oQqwToH4igpoM1SwaQzZU2jebFmSIBCeS5ujOD9k10GcZ9PTrXRVtMXrnsQ5EGvZPduRMTNoAoPw00wbF81B5N'



stripe.api_key = app.config['STRIPE_SECRET_KEY']

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.urandom(24)
    env = os.environ['DATABASE_URL'] = 'postgres://yycyfqgyyohwrf:1c2693cc568cb74986c58fc95bed0b6108e93614b710070252356a769735477c@ec2-34-198-31-223.compute-1.amazonaws.com:5432/d9vvnc5cts47mn'
    SQLALCHEMY_DATABASE_URI = env

@app.route('/')
def index():
    '''
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1I9X9XDE2fV8oQqwJEAnZA13',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks',_external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index',_external=True),
    )
    '''
    return render_template('index.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/signup', methods=["GET","POST"])
def signup():
    name = request.args.get('name')
    email = request.args.get('email')
    password = request.args.get('password')
    password_hash = generate_password_hash(password)
    account = Table('bashmenttbl',metadata,autoload=True)
    engine.execute(account.insert(),name=name,email=email,password=password_hash)
    # return jsonify({'user added': True})
    return render_template('signup.html')

@app.route('/login',methods=["GET","POST"])
def login():
    email_entered = request.args.get('email')
    password_entered = request.args.get('password')
    user = session.query(Accounts).filter(or_(Accounts.email == email_entered)).first()
    if user is not None and check_password_hash(user.password,password_entered):
        return jsonify({'signed_in': True})
    return render_template('login.html')

@app.route('/stripe_pay')
def stripe_pay():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': 'price_1I9X9XDE2fV8oQqwJEAnZA13',
            'quantity': 1,
           
        }],
        mode='payment',
        success_url=url_for('thanks',_external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index',_external=True),
    )
    return {'checkout_session_id':session['id'],'checkout_public_key':app.config['STRIPE_PUBLIC_KEY']}

@app.route('/stripe_pay2')
def stripe_pay2():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            
            'price': 'price_1I9ZVpDE2fV8oQqw9zWX31FR',
            'quantity': 1,
            
        }],
        mode='payment',
        success_url=url_for('thanks',_external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index',_external=True),
    )
    return {'checkout_session_id':session['id'],'checkout_public_key':app.config['STRIPE_PUBLIC_KEY']}

@app.route('/stripe_pay3')
def stripe_pay3():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
           
            'price': 'price_1I9Zg4DE2fV8oQqwRlgyxyXf',
            'quantity': 1,
        }],
        mode='payment',
        success_url=url_for('thanks',_external=True) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=url_for('index',_external=True),
    )
    return {'checkout_session_id':session['id'],'checkout_public_key':app.config['STRIPE_PUBLIC_KEY']}

  

@app.route('/stripe_webhook', methods=['POST'])
def stripe_webhook():
    print('WEBHOOK CALLED')

    if request.content_length > 1024 * 1024:
        print('REQUEST TOO BIG')
        abort(400)
    payload = request.get_data()
    sig_header = request.environ.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = 'whsec_6BImjLSSvA5cXDHqNLEGliHuOld3IvbE'
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print('INVALID PAYLOAD')
        return {}, 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print('INVALID SIGNATURE')
        return {}, 400

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(session)
        line_items = stripe.checkout.Session.list_line_items(session['id'], limit=1)
        print(line_items['data'][0]['description'])
    return {}

if __name__ == '__main__':
    app.run(debug=True)