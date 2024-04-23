from app import db
from app.models.user import User
# from app.models.user import Game
from flask import Blueprint, jsonify, make_response, abort, request
from app.helper_functions import *


users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("", methods=["POST"])
def create_user():
    request_body = request.get_json()
    user_data = validate_user(request_body)

    try:
        user = User.from_dict(user_data)
        db.session.add(user)
        db.session.commit()

        return make_response({"user": user.to_dict()}, 201)

    except KeyError:
        abort(make_response(
            {'Invalid data. Must include username and password.'}, 400))


@users_bp.route("/<user_id>", methods=["GET"])
def get_user(user_id):
    user = validate_model(User, user_id)

    return {"user": user.to_dict()}


@users_bp.route("/authentication", methods=["GET"])
def login_user():
    request_body = request.get_json()
    user = validate_user_login(
        request_body["username"], request_body["password"])

    return {"user": user.to_dict()}


@users_bp.route("/<user_id>/games", methods=["GET"])
def get_all_user_games(user_id):
    user = validate_model(User, user_id)
    user_response = [game.to_dict() for game in user.games]

    return jsonify(user_response), 200


@users_bp.route("/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = validate_model(User, user_id)

    db.session.delete(user)
    db.session.commit()

    return make_response({"details":  f"User: {user.user_id} deleted"})
