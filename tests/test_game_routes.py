from app.models.game import Game
from app.models.guess import Guess
from app.models.client import Client
import pytest


def test_create_game(client, new_client):
    data = {
        "lives": 10,
        "difficulty_level": 4,
        "num_min": 0,
        "num_max": 7,
        "client_id": new_client.client_id
    }
    response = client.post("/games", json=data)
    assert response.status_code == 201
    assert "game" in response.get_json()


def test_get_all_games(client, new_game):
    response = client.get("/games")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_get_one_game(client, new_game):
    response = client.get(f"/games/{new_game.game_id}")
    assert response.status_code == 200
    assert "game" in response.get_json()


def test_delete_game(client, new_game):
    response = client.delete(f"/games/{new_game.game_id}")
    assert response.status_code == 201
    assert "details" in response.get_json()


def test_add_guess_to_game(client, new_game):
    data = {
        "guess": "test_guess"
    }
    response = client.post(f"/games/{new_game.game_id}/guesses", json=data)
    assert response.status_code == 201
    assert "game" in response.get_json()


def test_get_all_guesses(client, new_game, new_guess):
    response = client.get(f"/games/{new_game.game_id}/guesses")
    assert response.status_code == 200
    assert len(response.get_json()) == 1
