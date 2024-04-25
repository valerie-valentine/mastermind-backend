import pytest
from app import create_app, db
from app.models.game import Game
from app.models.client import Client
from app.models.guess import Guess


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

    with app.app_context():
        db.create_all()
        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def new_game():
    return {
        "difficulty_level": 4,
        "num_min": 0,
        "num_max": 7,
        "lives": 10
    }


@pytest.fixture
def new_client():
    return Client(name="Test Client")


@pytest.fixture
def new_guess():
    return {"guess": 1111}


@pytest.fixture
def new_game_with_client(new_game, new_client):
    new_game["client_id"] = new_client.id
    return new_game
