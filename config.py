import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

def get_huggingface_token():
    # Retrieve the Hugging Face token from the environment
    return os.getenv("HUGGINGFACEHUB_API_TOKEN")

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'database.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.getenv('MAIL_PORT', 587)
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
   
    # Use the function to get the Hugging Face token
    HUGGINGFACE_TOKEN = get_huggingface_token()
   
    BASE_MODEL = os.getenv('BASE_MODEL', 'mistralai/Mistral-7B-v0.1')
    MODEL_NAME = os.getenv('MODEL_NAME', 'Malekhmem/ActiaMistral')

    GENERATION_CONFIG = {
        'do_sample': True,
        'top_p': 0.9,
        'top_k': 50,
        'temperature': 0.7,  # Corrected typo here
        'max_new_tokens': 10000,
        'repetition_penalty': 1.5,
        'pad_token_id': None
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

# Map configuration names to their respective classes
config_by_name = {
    'dev': DevelopmentConfig,
    'prod': ProductionConfig,
    'test': TestingConfig
}