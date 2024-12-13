from flask import make_response, abort, request
from app.models.game import Game
from app.models.guess import Guess
from app.models.client import Client
from app.helpers.model_utils import create_model
from app.helpers.validations import *
from ..db import db


def generate_game(request):
    request_body = request.get_json()
    game_data = ensure_valid_game_data(request_body)

    if "client_id" in request_body:
        client = validate_model_by_id(Client, request_body["client_id"])
        game_data["client_id"] = client.client_id

    return create_model(Game, game_data)


def retrieve_game(game_id):
    game = validate_model_by_id(Game, game_id)
    return {"game": game.to_dict()}, 200


def retrieve_all_games():
    query = db.select(Game).order_by(Game.game_id)
    games = db.session.scalars(query)
    game_response = [game.to_dict() for game in games]
    return game_response, 200


def remove_game(game_id):
    game = validate_model_by_id(Game, game_id)
    db.session.delete(game)
    db.session.commit()
    return make_response({"details": f"Game {game_id} deleted successfully"}, 204)


def add_guess_to_game(game_id, request):
    game = validate_model_by_id(Game, game_id)
    request_body = request.get_json()
    guess_data = ensure_valid_guess_data(game, request_body["guess"])
    client = validate_model_by_id(Client, request_body.get(
        "client_id")) if "client_id" in request_body else None

    guess = Guess.from_dict(guess_data)
    guess.check_client_guess(game)
    game.check_game_over(guess, client)
    guess.game = game

    db.session.add(guess)
    db.session.commit()

    return make_response({"game": game.to_dict()}, 201)


def retrieve_all_guesses(game_id):
    game = validate_model_by_id(Game, game_id)
    guess_response = [guess.to_dict() for guess in game.guesses]
    return guess_response, 200


def generate_hint(game_id):
    game = validate_model_by_id(Game, game_id)
    hint = game.generate_hint()
    return hint, 200
