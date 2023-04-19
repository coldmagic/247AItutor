from main import app, db

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Define the Chat model
class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(50), nullable=False)  # Add a subject column
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref=db.backref('chats', lazy=True))

def create_database():
    # Wrap the database creation in a try-except block
    try:
        # Create the database tables using the current app context
        with app.app_context():
            db.create_all()
        print("Database created successfully")
    except Exception as e:
        # Print any exceptions that occur during the database creation
        print(f"Error creating the database: {e}")

if __name__ == '__main__':
    create_database()
