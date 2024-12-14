# controllers/client_controller.py
from flask import make_response
from app.models.client import Client
from app.helpers.model_utils import create_model
from app.helpers.validations import *
from ..db import db


def create_user(request):
    request_body = request.get_json()
    client_data = ensure_valid_client_data(request_body)
    return create_model(Client, client_data)


def get_user(client_id):
    client = validate_model_by_id(Client, client_id)
    return {"client": client.to_dict()}, 200


def login_user(request):
    request_body = request.get_json()
    validated_client = ensure_valid_client_login(request_body)
    return {"client": validated_client.to_dict()}, 200


def get_user_games(client_id):
    client = validate_model_by_id(Client, client_id)
    client_response = [game.to_dict() for game in client.games]
    return client_response, 200


def delete_user(client_id):
    client = validate_model_by_id(Client, client_id)
    db.session.delete(client)
    db.session.commit()
    return make_response("", 204)


def get_winning_clients():
    query = db.select(Client).order_by(Client.score.desc()).limit(10)
    top_players = db.session.scalars(query)
    return [client.to_dict() for client in top_players], 200
