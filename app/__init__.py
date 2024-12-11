# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_bcrypt import Bcrypt
# import os
# from dotenv import load_dotenv
# from flask_cors import CORS

# db = SQLAlchemy()
# migrate = Migrate()
# load_dotenv()
# bcrypt = Bcrypt()


# def create_app(test_config=None):
#     app = Flask(__name__)
#     app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#     if test_config is None:
#         app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#             "SQLALCHEMY_DATABASE_URI")
#         # app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#         #     "HEROKU_DATABASE_URI")

#     else:
#         app.config["TESTING"] = True
#         app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#             "SQLALCHEMY_TEST_DATABASE_URI")

#     # Import models here for Alembic setup
#     from app.models.game import Game
#     from app.models.guess import Guess
#     from app.models.client import Client

#     # Initialize extensions
#     db.init_app(app)
#     migrate.init_app(app, db)
#     bcrypt.init_app(app)

#     # Register Blueprints here
#     from .routes.game_routes import games_bp
#     app.register_blueprint(games_bp)

#     from .routes.client_routes import clients_bp
#     app.register_blueprint(clients_bp)

#     CORS(app)
#     return app


# def create_app(config=None):
#     app = Flask(__name__)

#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
#         'SQLALCHEMY_DATABASE_URI')

#     if config:
#         # Merge `config` into the app's configuration
#         # to override the app's default settings for testing
#         app.config.update(config)

#     db.init_app(app)
#     migrate.init_app(app, db)

#     # Register Blueprints here
#     app.register_blueprint(client_bp)
#     app.register_blueprint(game_bp)

#     return app


from flask import Flask
from .db import db, migrate, bcrypt
from .models import client, game, guess
from .routes.client_routes import bp as client_bp
from .routes.new_game_routes import bp as game_bp
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

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register Blueprints here
    app.register_blueprint(game_bp)
    app.register_blueprint(client_bp)

    CORS(app)
    return app
