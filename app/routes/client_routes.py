from app.models.client import Client
from app.models.game import Game
from flask import Blueprint, make_response, abort, request
from app.helpers.model_utils import create_model
from app.helpers.validations import *
from ..db import db


bp = Blueprint("clients", __name__, url_prefix="/clients")

# MAKE MY CREATE ROUTES CONSISTENT  WITH ALL MY OTHER ROUTES!!!


@bp.route("", methods=["POST"])
def create_client():
    request_body = request.get_json()
    client_data = validate_client_data(request_body)
    return create_model(Client, client_data)


@bp.route("/<client_id>", methods=["GET"])
def get_client(client_id):
    client = validate_model(Client, client_id)

    return {"client": client.to_dict()}, 200


@bp.route("/authentication", methods=["POST"])
def login_client():
    request_body = request.get_json()
    validated_client = validate_client_login(request_body)

    return {"client": validated_client.to_dict()}, 200


@bp.route("/<client_id>/games", methods=["GET"])
def get_all_client_games(client_id):
    client = validate_model(Client, client_id)
    client_response = [game.to_dict() for game in client.games]

    return client_response, 200


@bp.route("/<client_id>", methods=["DELETE"])
def delete_client(client_id):
    client = validate_model(Client, client_id)

    db.session.delete(client)
    db.session.commit()

    return make_response({"details":  f"Client: {client.client_id} deleted"}, 204)


@bp.route("/top_players", methods=["GET"])
def get_winning_client():
    query = db.select(Client).order_by(Client.score.desc()).limit(10)
    top_players = db.session.scalars(query)
    clients_response = [client.to_dict_winners() for client in top_players]

    return clients_response, 200

# IDEALLY WANT TO USE THIS BUT WOULD HAVE TO REFACTOR HOW TO GAMES ARE CREATED ON FE
# @bp.route("/<client_id>/games", methods=["POST"])
# def create_game_with_client(client_id):
#     client = validate_model(Client, client_id)

#     request_body = request.get_json()
#     game_data = validate_game_data(request_body)
#     game_data["client_id"] = client.client_id
#     return create_model(Game, game_data)
