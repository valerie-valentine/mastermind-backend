from flask import Flask
from .db import db, migrate, bcrypt
from .models import client, game, guess
from .routes.client_routes import bp as client_bp
from .routes.game_routes import bp as game_bp
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if test_config is None:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
        # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        #     "HEROKU_DATABASE_URI")

    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Initialize db extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register Blueprints here
    app.register_blueprint(game_bp)
    app.register_blueprint(client_bp)

    CORS(app)
    return app
