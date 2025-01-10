import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'databasetibou.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    HUGGINGFACE_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')
    BASE_MODEL = os.getenv('BASE_MODEL')
    MODEL_NAME = os.getenv('MODEL_NAME')

    GENERATION_CONFIG = {
        'do_sample': True, 
        'top_p': 0.9,
        'top_k': 50,
        'temperature': 0.7,  # Vérifiez que l'orthographe est correcte
        'max_new_tokens': 1000,
        'repetition_penalty': 1.5, 
        'pad_token_id': None,
        'quant_method': 'dynamic'
    }

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig,
    test=TestingConfig
)
