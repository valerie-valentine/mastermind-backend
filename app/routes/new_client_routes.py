from flask import Blueprint, request
from app.controllers.client_controller import *

bp = Blueprint("clients", __name__, url_prefix="/clients")


@bp.route("", methods=["POST"])
def create_client():
    return create_user(request)


@bp.route("/<client_id>", methods=["GET"])
def get_client(client_id):
    return get_user(client_id)


@bp.route("/authentication", methods=["POST"])
def login_client():
    return login_user(request)


@bp.route("/<client_id>/games", methods=["GET"])
def get_client_game(client_id):
    return get_user_games(client_id)


@bp.route("/<client_id>", methods=["DELETE"])
def delete_client(client_id):
    return delete_user(client_id)


@bp.route("/top_players", methods=["GET"])
def get_top_players():
    return get_winning_clients()
