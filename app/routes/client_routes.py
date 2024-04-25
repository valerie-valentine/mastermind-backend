from app import db, bcrypt
from app.models.client import Client
from flask import Blueprint, jsonify, make_response, abort, request
from app.helper_functions import *


clients_bp = Blueprint("clients", __name__, url_prefix="/clients")


@clients_bp.route("", methods=["POST"])
def create_client():
    request_body = request.get_json()
    client_data = validate_client(request_body)
    hashed_password = bcrypt.generate_password_hash(
        client_data["password"]).decode('utf-8')

    try:
        client = Client.from_dict(client_data)
        client.password = hashed_password
        db.session.add(client)
        db.session.commit()

        return make_response({"client": client.to_dict()}, 201)

    except KeyError:
        abort(make_response(
            {'details': f'Failed to create client. Please check your input data'}, 400))


@clients_bp.route("/<client_id>", methods=["GET"])
def get_client(client_id):
    client = validate_model(Client, client_id)

    return {"client": client.to_dict()}


@clients_bp.route("/authentication", methods=["POST"])
def login_client():
    request_body = request.get_json()
    validated_client = validate_client_login(request_body)
    print(request_body)

    return {"client": validated_client.to_dict()}, 200


@clients_bp.route("/<client_id>/games", methods=["GET"])
def get_all_client_games(client_id):
    client = validate_model(Client, client_id)
    client_response = [game.to_dict() for game in client.games]

    return jsonify(client_response), 200


@clients_bp.route("/<client_id>", methods=["DELETE"])
def delete_client(client_id):
    client = validate_model(Client, client_id)

    db.session.delete(client)
    db.session.commit()

    return make_response({"details":  f"Client: {client.client_id} deleted"})


@clients_bp.route("/top_players", methods=["GET"])
def get_winning_client():
    top_clients = Client.query.order_by(
        Client.score.desc()).all()
    clients_response = [client.to_dict() for client in top_clients]

    return jsonify(clients_response), 200
