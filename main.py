# main.py
from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash
from server.chat_gpt import ask_kate
from server.models import init_db, create_user, get_user_by_email, add_chat, get_chats
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
@login_required
def index():
    # Render the main chat page
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
@login_required
def chat():
    # Receive user message and return AI response
    data = request.get_json()
    subject = data.get('subject')
    message = data.get('message')

    ai_response = ask_kate(message)

    if 'user_id' in session:
        add_chat(session['user_id'], subject, message, ai_response)  # Updated to include the subject

    return jsonify({'response': ai_response})

@app.route('/api/chats', methods=['GET'])
@login_required
def chats():
    # Retrieve the chat history for the current user
    chats = get_chats(session['user_id'])
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
            return render_template('login.html', error='Invalid email or password')

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

@app.route('/logout')
def logout():
    # Log out the user by removing the user_id from the session
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81)
