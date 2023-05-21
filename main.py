from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from server.chat_gpt import ask_kate
from server.models import init_db, create_user, get_user_by_email, add_chat, get_chats
from server.payfast import generate_signature, pfValidSignature, pfValidIP, pfValidPaymentData, pfValidServerConfirmation
import os
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ['app_secret_key']

# Initialize the database with the Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
init_db(app)

# Decorator function to ensure user is logged in before accessing certain routes
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/home')
@login_required
def index():
    # Render the main chat page
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    # Receive user message and return AI response
    data = request.get_json()
    message = data.get('message')

    ai_response = ask_kate(message)

    if 'user_id' in session:
        add_chat(session['user_id'], data.get('subject'), message, ai_response)

    return jsonify({'response': ai_response})

@app.route('/api/chats/<subject>', methods=['GET'])
@login_required
def chats(subject):
    # Retrieve the chat history for the current user and the selected subject
    chats = get_chats(session['user_id'], subject)
    chat_data = [
        {'subject': chat.subject, 'message': chat.message, 'response': chat.response} for chat in chats
    ]

    return jsonify(chat_data)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(request.form)  # Print form data

        user = get_user_by_email(email)
        print(user)  # Print user object

        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid email or password') #added comment

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        print(request.form)  # Print form data

        existing_user = get_user_by_email(email)
        if existing_user:
            flash('A user with this email already exists', 'danger')
            print('A user with this email already exists')
        else:
            user = create_user(name, email, password)
            session['user_id'] = user.id
            flash('Registration successful', 'success')
            print('Registration successful')
            return redirect(url_for('index'))

    return render_template('register.html')

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Assuming `user` and other necessary variables are defined elsewhere in your code
    user = get_current_user()  # replace with your actual function for getting the current user

    # Prepare the data for PayFast
    pf_data = {
        "merchant_id": "10980749",
        "merchant_key": "aa3a4xa7jdrda",
        "return_url": url_for('index', _external=True),
        "notify_url": url_for('notify', _external=True),
        "cancel_url": url_for('cancel', _external=True),
        "m_payment_id": "UniqueId",  # replace with your actual unique ID
        "amount": "997.00",
        "item_name": "Kate Academy AI - Monthly Subscription",
        "item_description": "Kate Academy AI - Monthly Subscription",
        "email_confirmation": "1",
        "confirmation_address": user.email,
        "payment_method": "cc",
        "name_first": user.first_name,
        "name_last": user.last_name,
        "email_address": user.email
        # Add other necessary variables here
    }

    # Generate the signature
    passphrase = 'jt7NOE43FZPn'  # replace with your actual passphrase
    signature = generate_signature(pf_data, passphrase)

    return render_template('checkout.html', user=user, signature=signature)

@app.route('/notify', methods=['POST'])
def notify():
    # Get the data sent by PayFast
    data = request.form.to_dict()

    # Verify the signature
    passphrase = 'your_passphrase'  # replace with your actual passphrase
    if not pfValidSignature(data, passphrase):
        return 'Invalid signature', 400

    # Check that the ITN has come from a valid PayFast domain
    if not pfValidIP():
        return 'Invalid host', 400

    # Compare the payment data
    expected_amount = 997.00  # replace with your actual expected amount
    if not pfValidPaymentData(expected_amount, data):
        return 'Invalid payment data', 400

    # Confirm the details with a server request
    if not pfValidServerConfirmation(data, passphrase):
        return 'Failed to confirm details with server', 400

    # The signatures match, so the data is valid
    # Here you can update your database, send confirmation emails, etc.
    pass  # replace with your actual code

    # Return a 200 OK response
    return '', 200



@app.route('/logout')
def logout():
    # Log out the user by removing the user_id from the session
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
     app.run(host='0.0.0.0', port=81)
