from app import db
from app.models.game import Game
from app.models.guess import Guess
from app.models.client import Client
from flask import Blueprint, jsonify, make_response, abort, request
from app.helper_functions import *


def test_create_client(client):
    data = {
        "username": "testuser",
        "password": "password123",
        "email": "test@gmail.com"
    }
    response = client.post("/clients", json=data)
    assert response.status_code == 201
    assert "client" in response.json
    assert response.json["client"]["username"] == "testuser"

    new_client = Client.query.filter_by(username="testuser").first()
    assert new_client is not None


def test_get_client(client):
    new_client = Client(username="testuser", password="password123")
    db.session.add(new_client)
    db.session.commit()

    response = client.get(f"/clients/{new_client.client_id}")
    assert response.status_code == 200
    assert "client" in response.json
    assert response.json["client"]["username"] == "testuser"


def test_delete_client(client):
    new_client = Client(username="testuser", password="password123")
    db.session.add(new_client)
    db.session.commit()

    response = client.delete(f"/clients/{new_client.client_id}")
    assert response.status_code == 200
    assert "details" in response.json
    assert response.json["details"] == f"Client: {
        new_client.client_id} deleted"

    deleted_client = Client.query.get(new_client.client_id)
    assert deleted_client is None


def test_get_top_players(client):
    client1 = Client(username="user1", password="password123", score=100)
    client2 = Client(username="user2", password="password456", score=200)
    client3 = Client(username="user3", password="password789", score=150)
    db.session.add_all([client1, client2, client3])
    db.session.commit()

    response = client.get("/clients/top_players")
    assert response.status_code == 200
    assert len(response.json) == 3
    assert response.json[0]["username"] == "user2"
