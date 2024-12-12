from ..db import db
from app.models.game import Game
from app.models.guess import Guess
from app.models.client import Client
from flask import Blueprint, make_response, abort, request
from app.helper_functions import *


bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route("", methods=["POST"])
def create_game():
    request_body = request.get_json()
    game_data = validate_game_data(request_body)

    if 'client_id' in request_body and request_body['client_id']:
        client = validate_model(Client, request_body['client_id'])
        game_data["client_id"] = client.id
    return create_model(Game, game_data)


@bp.route("/<game_id>", methods=["GET"])
def get_one_game(game_id):
    game = validate_model(Game, game_id)

    return {"game": game.to_dict()}


@bp.route("", methods=["GET"])
def get_all_games():
    # games = Game.query.all()
    # games_response = [game.to_dict() for game in games]
    query = db.select(Game).order_by(Game.id)
    games = db.session.scalars(query)
    games_response = [game.to_dict() for game in games]

    # new version of flask doesn't require jsonify lists
    # return jsonify(games_response), 200
    return games_response


@bp.route("/<game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = validate_model(Game, game_id)

    db.session.delete(game)
    db.session.commit()

    return make_response({"details": f"Game {game_id} deleted successfully"}, 204)


@bp.route("/<game_id>/guesses", methods=["POST"])
# DOUBLE CHECK THIS STILL WORKS!! - It does but verify everything again!
def add_guess_to_game(game_id):
    game = validate_model(Game, game_id)
    request_body = request.get_json()
    guess_data = validate_guess_data(game, request_body["guess"])
    # Have to set client to None if no clientid is provided otherwise run into error when check_game_over is called
    client_id = request_body.get("client_id")
    client = validate_model(Client, client_id) if client_id else None

    try:
        guess = Guess.from_dict(game, guess_data)
        game.check_game_over(guess, client)
        guess.game = game

    except KeyError:
        abort(make_response({"details": "Invalid data"}), 400)

    db.session.add(guess)
    db.session.commit()

    return make_response({"game": game.to_dict()}, 201)


@bp.route("/<game_id>/guesses", methods=["GET"])
def get_all_guesses(game_id):
    game = validate_model(Game, game_id)
    guess_response = [guess.to_dict() for guess in game.guesses]

    # return jsonify(guess_response), 200
    return guess_response


@bp.route("/<game_id>/hint", methods=["GET"])
def get_hint(game_id):
    game = validate_model(Game, game_id)
    hint = generate_hint(game)

    # maybe just return hint? Check if still gives status 200
    return hint
