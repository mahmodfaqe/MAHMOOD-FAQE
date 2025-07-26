import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_DATABASE_URI = "postgresql://bokweadmin:StrongPassword123!@your-endpoint:5432/bokwe-db"



    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'your_default_jwt_secret_key')

    BABEL_DEFAULT_LOCALE = 'en'
    LANGUAGES = ['en', 'ku', 'ar']

