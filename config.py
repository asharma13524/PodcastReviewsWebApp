from os import environ, path
from dotenv import load_dotenv


basedir = path.abspath(path.dirname('__file__'))
load_dotenv(path.join(basedir, '.env'))


class Config():
    """Config from .env file"""
    SECRET_KEY = environ.get('SECRET_KEY')
    FLASK_APP = environ.get('FLASK_APP')
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')



class Production(Config):
    """Prod Config"""

    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    PROD_DATABASE_URI = environ.get('PROD_DATABASE_URI')


class DevConfig(Config):
    """Dev Config"""

    # env
    FLASK_ENV = environ.get("FLASK_ENV")
    DEBUG = True
    TESTING = True

    # DB
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    # Flask Assets
    ASSETS_DEBUG = True
    LESS_BIN = environ.get('LESS_BIN')
    LESS_RUN_IN_DEBUG = True

    # Static Assets
    COMPRESSOR_DEBUG = True
    ASSETS_AUTO_BUILD = True
