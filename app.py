from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from auth import auth, User, db, Conversation, Disscution
from chat import chat, chatbot
from config import config_by_name
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask application
app = Flask(__name__)
config_name = os.getenv('FLASK_CONFIG', 'dev')
app.config.from_object(config_by_name[config_name])

# Initialize Flask extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'
migrate = Migrate(app, db)

# Register blueprints
app.register_blueprint(auth, url_prefix='/auth')  # Auth blueprint with /auth prefix
app.register_blueprint(chat, url_prefix='/chat')  # Chat blueprint with /chat prefix

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Default route for '/'
@app.route('/')
def index():
    return redirect(url_for('auth.login'))  # Redirect to login page

# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Route for handling chatbot messages
@app.route('/ask', methods=['POST'])
@login_required
def ask():
    try:
        # Get message and conversation ID
        message = str(request.form['messageText'])
        conversation_id = request.form.get('conversationId', type=int)

        app.logger.debug(f"Received message: {message}")

        # If conversation does not exist, create a new one
        if not conversation_id:
            title = ' '.join(message.split()[:3])
            new_conversation = Conversation(user_id=current_user.id, title=title)
            db.session.add(new_conversation)
            db.session.commit()
            conversation_id = new_conversation.id

        # Save user message
        user_message = Disscution(conversation_id=conversation_id, content=message, is_user=True)
        db.session.add(user_message)
        db.session.commit()

        # Generate chatbot response
        bot_response = chatbot(message)
        if not bot_response:
            bot_response = "Sorry, the system encountered an issue. Please try again later."

        # Save chatbot response
        bot_message = Disscution(conversation_id=conversation_id, content=bot_response, is_user=False)
        db.session.add(bot_message)
        db.session.commit()

        app.logger.debug(f"Bot response: {bot_response}")
        print("Bot response:", bot_response)

        return jsonify({'status': 'OK', 'answer': bot_response, 'conversationId': conversation_id})

    except Exception as e:
        app.logger.error(f"Error: {e}", exc_info=True)
        return jsonify({'status': 'ERROR', 'answer': f'Sorry, there was an error processing your request: {str(e)}'})

# Main block
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure all tables are created
    app.run(host='0.0.0.0', port=5000)