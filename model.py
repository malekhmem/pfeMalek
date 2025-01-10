import os
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, BitsAndBytesConfig
import torch

# Configuration du modèle
model_name = "Malekhmem/ActiaMistral"

# Charger le token Hugging Face
huggingface_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not huggingface_token:
    raise EnvironmentError("Hugging Face API token is missing. Set it as an environment variable.")

# Charger le modèle avec une configuration optimisée pour réduire l'utilisation mémoire
bnb_config = BitsAndBytesConfig(
    load_in_8bit=True,  # Active le chargement 8 bits
    llm_int8_threshold=6.0
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

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

try:
    tokenizer = AutoTokenizer.from_pretrained(model_name, token=huggingface_token)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto",
        quantization_config=bnb_config
    )
except Exception as e:
    raise RuntimeError(f"Failed to load model or tokenizer: {e}")

# Configuration de génération
generation_config = GenerationConfig(
    max_length=300,
    top_p=0.9,
    top_k=50,
    early_stopping=True,
    do_sample=True
)

def generate_response(input_text):
    """
    Génère une réponse basée sur le texte d'entrée.
    """
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
        output = model.generate(
            input_ids,
            max_length=generation_config.max_length,
            top_p=generation_config.top_p,
            top_k=generation_config.top_k,
            early_stopping=generation_config.early_stopping,
            do_sample=generation_config.do_sample
        )
        return tokenizer.decode(output[0], skip_special_tokens=True)
    except torch.cuda.OutOfMemoryError:
        torch.cuda.empty_cache()
        return "Sorry, the model ran out of memory. Please try again later."
    except Exception as e:
        return f"An error occurred during text generation: {e}"
