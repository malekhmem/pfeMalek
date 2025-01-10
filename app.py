from flask import Flask, render_template
from auth import auth  # Import the auth blueprint
from model import db, User, Conversation, Discussion  # Ensure these models are correctly imported
from flask_login import LoginManager

app = Flask(__name__)

# Configuration settings
app.config['SECRET_KEY'] = 'your_secret_key'  # Add your secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Replace with your database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable unnecessary alerts

# Initialize the database with Flask
db.init_app(app)

# Setup Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register the blueprint
app.register_blueprint(auth, url_prefix='/auth')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
