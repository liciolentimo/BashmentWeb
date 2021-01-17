from flask import Flask, render_template, url_for
import stripe

app = Flask(__name__)

app.config['STRIPE_PUBLIC_KEY'] = 'pk_test_mWaJhKb35BpMP15bfsE1CB9j00aBE0OgQT'
app.config['STRIPE_SECRET_KEY'] = 'sk_test_51EkSfRDE2fV8oQqwToH4igpoM1SwaQzZU2jebFmSIBCeS5ujOD9k10GcZ9PTrXRVtMXrnsQ5EGvZPduRMTNoAoPw00wbF81B5N'

stripe.api_key = app.config['STRIPE_SECRET_KEY']

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

@app.route('/signup')
def signup():
    return render_template('signup.html')

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