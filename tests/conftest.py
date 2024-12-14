import pytest
from sqlalchemy import select
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
def new_client(app):
    new_client = Client(
        email="test@example.com",
        password="test_password",
        username="test_user",
        client_id=1
    )
    db.session.add(new_client)
    db.session.commit()

    return client


@pytest.fixture
def new_game_with_id(app):
    new_game = Game(
        lives=10,
        difficulty_level=4,
        num_min=0,
        num_max=7,
        client_id=1,
        answer="1234"
    )

    db.session.add(new_game)
    db.session.commit()

    return new_game


@pytest.fixture
def new_game_without_id(app):
    new_game = Game(
        lives=10,
        difficulty_level=4,
        num_min=0,
        num_max=7,
        answer="1234"
    )

    db.session.add(new_game)
    db.session.commit()

    return new_game


@pytest.fixture
def guess_belongs_to_game(app, new_game_without_id):
    query = select(Game).where(Game.game_id == new_game_without_id.game_id)
    game = db.session.execute(query).scalars().first()

    new_guess = Guess(
        guess="1111"
    )

    # Associate the guess with the game
    new_guess.game = game
    game.guesses.append(new_guess)
    db.session.commit()

    return new_guess
