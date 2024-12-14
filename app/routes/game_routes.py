from app.models.game import Game
from app.models.guess import Guess
from app.models.client import Client
from flask import Blueprint, make_response, abort, request
from app.helpers.model_utils import create_model
from app.helpers.validations import *
from ..db import db


bp = Blueprint("games", __name__, url_prefix="/games")


# @bp.route("", methods=["POST"])
# def create_game():
#     request_body = request.get_json()
#     game_data = ensure_valid_game_data(request_body)

#     if 'client_id' in request_body and request_body['client_id']:
#         client = validate_model_by_id(Client, request_body['client_id'])
#         game_data["client_id"] = client.client_id
#     return create_model(Game, game_data)


@bp.route("", methods=["POST"])
def create_game():
    request_body = request.get_json()
    game_data = ensure_valid_game_data(request_body)

    try:
        game = Game.from_dict(game_data)

        if not game.answer:
            return make_response({"details": "Error: Game answer not generated correctly."}, 400)

        if 'client_id' in request_body and request_body['client_id']:
            client = validate_model_by_id(Client, request_body['client_id'])
            game.client = client

    except KeyError:
        abort(make_response({"details": "Invalid data"}), 400)

    db.session.add(game)
    db.session.commit()

    return make_response({"game": game.to_dict()}, 201)


@bp.route("/<game_id>", methods=["GET"])
def get_one_game(game_id):
    game = validate_model_by_id(Game, game_id)

    return {"game": game.to_dict()}, 200


@bp.route("", methods=["GET"])
def get_all_games():
    query = db.select(Game).order_by(Game.game_id)
    games = db.session.scalars(query)
    games_response = [game.to_dict() for game in games]

    # new version of flask doesn't require jsonify lists
    return games_response, 200


@bp.route("/<game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = validate_model_by_id(Game, game_id)

    db.session.delete(game)
    db.session.commit()

    return make_response({"details": f"Game {game_id} deleted successfully"}, 200)


@bp.route("/<game_id>/guesses", methods=["POST"])
def add_guess_to_game(game_id):
    game = validate_model_by_id(Game, game_id)
    request_body = request.get_json()
    guess_data = ensure_valid_guess_data(game, request_body["guess"])
    # Have to set client to None if no clientid is provided otherwise run into error when check_game_over is called
    client_id = request_body.get("client_id")
    client = validate_model_by_id(Client, client_id) if client_id else None

    try:
        guess = Guess.from_dict(guess_data)
        guess.check_client_guess(game)
        game.check_game_over(guess, client)
        guess.game = game

    except KeyError:
        abort(make_response({"details": "Invalid data"}), 400)

    db.session.add(guess)
    db.session.commit()

    return make_response({"game": game.to_dict()}, 201)


@bp.route("/<game_id>/guesses", methods=["GET"])
def get_all_guesses(game_id):
    game = validate_model_by_id(Game, game_id)
    guess_response = [guess.to_dict() for guess in game.guesses]

    return guess_response, 200


@bp.route("/<game_id>/hint", methods=["GET"])
def get_hint(game_id):
    game = validate_model_by_id(Game, game_id)
    hint = game.generate_hint()

    return hint, 200
