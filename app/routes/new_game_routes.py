from flask import Blueprint, request, abort, make_response
from app.controllers.game_controller import *

bp = Blueprint("games", __name__, url_prefix="/games")


@bp.route("", methods=["POST"])
def create_game():
    return generate_game(request)


@bp.route("/<game_id>", methods=["GET"])
def get_one_game(game_id):
    return retrieve_game(game_id)


@bp.route("", methods=["GET"])
def get_all_games():
    return retrieve_all_games()


@bp.route("/<game_id>", methods=["DELETE"])
def delete_game(game_id):
    return remove_game(game_id)


@bp.route("/<game_id>/guesses", methods=["POST"])
def add_guess_to_game_route(game_id):
    try:
        response = add_guess_to_game(game_id, request)
        return response
    except KeyError:
        abort(make_response({"details": "Invalid data"}), 400)


@bp.route("/<game_id>/guesses", methods=["GET"])
def get_all_guesses(game_id):
    return retrieve_all_guesses(game_id)


@bp.route("/<game_id>/hint", methods=["GET"])
def get_hint(game_id):
    return generate_hint(game_id)
