#Server/models.py: 
#This is a module that defines the User and Message models for your app using SQLAlchemy. 
#The User model has attributes such as id, username, email, password_hash, subscription and messages. 
#The Message model has attributes such as id, sender_id, receiver_id, content and timestamp. 
#The models also have methods for creating, updating and deleting instances in the database.


from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# Create a new user and save it to the database
def create_user(name, email, password):
    user = User(name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

# Retrieve a user by their email address
def get_user_by_email(email):
    return User.query.filter_by(email=email).first()

# Define the Chat model
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref=db.backref('chats', lazy=True))

# Add a new chat to the database
def add_chat(user_id, subject, message, response):
    chat = Chat(user_id=user_id, subject=subject, message=message, response=response)
    db.session.add(chat)
    db.session.commit()
    print(f"Chat saved to the database: {chat}")

# Retrieve all chats for a given user and subject
def get_chats(user_id, subject):
    return Chat.query.filter_by(user_id=user_id, subject=subject).all()

# Initialize the database
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
