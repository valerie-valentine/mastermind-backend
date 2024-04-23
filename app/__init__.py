from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
import os
from dotenv import load_dotenv
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()
bcrypt = Bcrypt()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "SQLALCHEMY_DATABASE_URI")

    # Import models here for Alembic setup
    from app.models.game import Game
    from app.models.guess import Guess
    from app.models.user import User

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register Blueprints here
    from .routes.game_routes import games_bp
    app.register_blueprint(games_bp)

    from .routes.user_routes import users_bp
    app.register_blueprint(users_bp)

    CORS(app)
    return app
