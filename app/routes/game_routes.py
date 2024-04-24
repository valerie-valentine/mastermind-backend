from app import db
from app.models.game import Game
from app.models.guess import Guess
from flask import Blueprint, jsonify, make_response, abort, request
from app.helper_functions import *


games_bp = Blueprint("games", __name__, url_prefix="/games")


@games_bp.route("", methods=["POST"])
def create_game():
    request_body = request.get_json()
    game_data = validate_game_data(request_body)
    generated_answer = random_number(
        game_data["difficulty_level"], request_body["num_min"], request_body["num_max"])

    try:
        game = Game.from_dict(game_data)
        game.answer = generated_answer

        if 'user_id' in request_body:
            user = validate_model(User, request_body['user_id'])
            game.user = user

        db.session.add(game)
        db.session.commit()

        return make_response({"game": game.to_dict()}, 201)

    except KeyError:
        abort(make_response({"details": "Invalid data"}), 400)


@games_bp.route("/<game_id>", methods=["GET"])
def get_one_game(game_id):
    game = validate_model(Game, game_id)

    return {"game": game.to_dict()}


@games_bp.route("", methods=["GET"])
def get_all_games():
    games = Game.query.all()
    games_response = [game.to_dict() for game in games]

    return jsonify(games_response), 200


@games_bp.route("/<game_id>", methods=["DELETE"])
def delete_game(game_id):
    game = validate_model(Game, game_id)

    db.session.delete(game)
    db.session.commit()

    return make_response({"details": game.game_id})


@games_bp.route("/<game_id>/guesses", methods=["POST"])
def add_guess_to_game(game_id):
    game = validate_model(Game, game_id)
    request_body = request.get_json()
    guess_data = validate_user_guess(game, request_body["guess"])
    correct_num, correct_loc = check_user_guess(game, guess_data)

    try:
        guess = Guess.from_dict(request_body)
        guess.correct_num = correct_num
        guess.correct_loc = correct_loc
        # guess.game_id = game.game_id
        guess.game = game
        db.session.add(guess)
        db.session.commit()

        return make_response({"guess": guess.to_dict()}, 201)

    except KeyError:
        abort(make_response({"details": "Invalid data"}), 400)


@games_bp.route("/<game_id>/guesses", methods=["GET"])
def get_all_guesses(game_id):
    game = validate_model(Game, game_id)
    guess_response = [guess.to_dict() for guess in game.guesses]

    return jsonify(guess_response), 200


@games_bp.route("/<game_id>/hint", methods=["GET"])
def get_hint(game_id):
    game = validate_model(Game, game_id)
    hint = generate_hint(game)

    return jsonify(hint), 200
