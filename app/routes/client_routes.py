from app.models.client import Client
from app.models.game import Game
from flask import Blueprint, make_response, abort, request
from app.helper_functions import *
from ..db import db, bcrypt


bp = Blueprint("clients", __name__, url_prefix="/clients")


# @bp.route("", methods=["POST"])
# def create_client():
#     request_body = request.get_json()
#     client_data = validate_client(request_body)
#     hashed_password = bcrypt.generate_password_hash(
#         client_data["password"]).decode('utf-8')

#     try:
#         client = Client.from_dict(client_data)
#         client.password = hashed_password
#         db.session.add(client)
#         db.session.commit()

#         return make_response({"client": client.to_dict()}, 201)

#     except KeyError:
#         abort(make_response(
#             {'details': f'Failed to create client. Please check your input data'}, 400))

@bp.route("", methods=["POST"])
def create_client():
    request_body = request.get_json()
    client_data = validate_client_data(request_body)
    return create_model(Client, client_data)


@bp.route("/<client_id>", methods=["GET"])
def get_client(client_id):
    client = validate_model(Client, client_id)

    return {"client": client.to_dict()}


@bp.route("/authentication", methods=["POST"])
def login_client():
    request_body = request.get_json()
    validated_client = validate_client_login(request_body)

    return {"client": validated_client.to_dict()}, 200


@bp.route("/<client_id>/games", methods=["GET"])
def get_all_client_games(client_id):
    client = validate_model(Client, client_id)
    client_response = [game.to_dict() for game in client.games]

    return client_response


@bp.route("/<client_id>", methods=["DELETE"])
def delete_client(client_id):
    client = validate_model(Client, client_id)

    db.session.delete(client)
    db.session.commit()

    return make_response({"details":  f"Client: {client.id} deleted"}, 204)


# @bp.route("/top_players", methods=["GET"])
# def get_winning_client():
#     top_clients = Client.query.order_by(
#         Client.score.desc()).limit(10).all()
#     clients_response = [client.to_dict_winners() for client in top_clients]

#     return clients_response

@bp.route("/top_players", methods=["GET"])
def get_winning_client():
    query = db.select(Client).order_by(Client.score.desc()).limit(10)
    top_players = db.session.scalars(query)
    clients_response = [client.to_dict_winners() for client in top_players]

    return clients_response

# IDEALLY WANT TO USE THIS BUT WOULD HAVE TO REFACTOR HOW TO GAMES ARE CREATED ON FE
# @bp.route("/<client_id>/games", methods=["POST"])
# def create_game_with_client(client_id):
#     client = validate_model(Client, client_id)

#     request_body = request.get_json()
#     game_data = validate_game_data(request_body)
#     game_data["client_id"] = client.id
#     return create_model(Game, game_data)
