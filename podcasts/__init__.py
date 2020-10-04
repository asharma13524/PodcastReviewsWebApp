from flask import Flask, blueprints
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap
from flask_assets import Environment
from flask_login import LoginManager
import os

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.ProdConfig")
    assets = Environment()

    # initializate DB, Marshmallow, Bootstrap, assets, login
    db.init_app(app)
    ma.init_app(app)
    Bootstrap(app)
    assets.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # import needed routes from application
        from .home import home
        from .profile import profile
        from .auth import auth

        # register blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(profile.profile_bp)
        app.register_blueprint(auth.auth_bp)


        # create all db models
        db.create_all()

        return app
