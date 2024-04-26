import pytest
from app import create_app, db
from app.models.game import Game
from app.models.client import Client
from app.models.guess import Guess
from flask.signals import request_finished


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def new_client_data(app):
    return {
        "email": "test@example.com",
        "password": "test_password",
        "username": "test_user"
    }


@pytest.fixture
def new_game_data(app):
    return {
        "lives": 10,
        "difficulty_level": 4,
        "num_min": 0,
        "num_max": 7,
        "answer": "1234"
    }


@pytest.fixture
def new_guess_data(app):
    return {
        "guess": "1234"
    }


@pytest.fixture
def new_client(app, new_client_data):
    client = Client.from_dict(new_client_data)
    db.session.add(client)
    db.session.commit()

    return client


@pytest.fixture
def new_game(app, new_game_data, new_client):
    game_data = new_game_data.copy()
    game_data["client_id"] = new_client.client_id
    game = Game.from_dict(game_data)

    db.session.add(game)
    db.session.commit()

    return game


@pytest.fixture
def new_guess(app, new_guess_data, new_game):
    guess_data = new_guess_data.copy()
    guess_data["game_id"] = new_game.game_id
    guess = Guess.from_dict(guess_data)

    db.session.add(guess)
    db.session.commit()

    return guess
