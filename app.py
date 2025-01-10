import os
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from auth import auth  # Import du blueprint
from model import generate_response  # Importation de la fonction de génération de réponse
from dotenv import load_dotenv

load_dotenv()

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'supersecretkey')

# Initialisation des extensions
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'  # Spécifier le blueprint pour la vue login
migrate = Migrate(app, db)

# Enregistrement du blueprint 'auth'
app.register_blueprint(auth, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Modèles de base de données
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    messages = db.relationship('Discussion', backref='conversation', lazy=True)


class Discussion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    is_user = db.Column(db.Boolean, default=True)


# Routes Flask
@app.route('/')
def index():
    if current_user.is_authenticated:
        conversations = Conversation.query.filter_by(user_id=current_user.id).all()
        return render_template('index.html', conversations=conversations)
    return redirect(url_for('auth.login'))

@app.route('/ask', methods=['POST'])
@login_required
def ask():
    try:
        message = request.form['messageText']
        conversation_id = request.form.get('conversationId', type=int)

        if not conversation_id:
            # Créer une nouvelle conversation
            title = ' '.join(message.split()[:3])  # Utiliser les premiers mots comme titre
            new_conversation = Conversation(user_id=current_user.id, title=title)
            db.session.add(new_conversation)
            db.session.commit()
            conversation_id = new_conversation.id

        # Sauvegarder le message utilisateur
        user_message = Discussion(conversation_id=conversation_id, content=message, is_user=True)
        db.session.add(user_message)
        db.session.commit()

        # Générer la réponse du bot
        bot_response = generate_response(message)  # Utilisation de la fonction de génération de réponse
        bot_message = Discussion(conversation_id=conversation_id, content=bot_response, is_user=False)
        db.session.add(bot_message)
        db.session.commit()

        return jsonify({'status': 'OK', 'answer': bot_response, 'conversationId': conversation_id})
    except Exception as e:
        return jsonify({'status': 'ERROR', 'answer': f'Error: {str(e)}'})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
