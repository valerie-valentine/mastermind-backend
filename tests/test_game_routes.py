

def test_create_game(client):
    # act
    game_data = {
        "lives": 10,
        "difficulty_level": 4,
        "num_min": 0,
        "num_max": 7,
    }

    # arrange
    response = client.post("/games", json=game_data)

    # assert
    assert response.status_code == 201
    assert "game" in response.get_json()


def test_create_game_with_client(client, new_client):
    # act
    game_data = {
        "lives": 10,
        "difficulty_level": 4,
        "num_min": 0,
        "num_max": 7,
        "client_id": 1
    }

    # arrange
    response = client.post("/games", json=game_data)

    # assert
    assert response.status_code == 201
    assert "game" in response.get_json()


def test_get_all_games(client, new_client, new_game_with_id, new_game_without_id):
    # arrange
    response = client.get("/games")

    # assert
    assert response.status_code == 200
    assert len(response.get_json()) == 2


def test_get_one_game(client, new_client, new_game_with_id):
    # arrange
    response = client.get(f"/games/{new_game_with_id.game_id}")

    # assert
    assert response.status_code == 200
    assert "game" in response.get_json()


def test_delete_game(client, new_client, new_game_with_id):
    # arrange
    response = client.delete(f"/games/{new_game_with_id.game_id}")

    # assert
    assert response.status_code == 200
    assert "details" in response.get_json()


def test_add_guess_to_game(client, new_game_without_id):
    # act
    data = {
        "guess": "1234"
    }

    # arrange
    response = client.post(
        f"/games/{new_game_without_id.game_id}/guesses", json=data)
    response_body = response.get_json()

    # assert
    assert response.status_code == 201
    assert "game" in response_body
    assert len(response_body) == 1
    assert response_body["game"]["guesses"] == [
        {"guess": "1234", "game_id": 1, "correct_num": 4, "correct_loc": 4, "guess_id": 1}]


def test_get_all_guesses(client, new_game_without_id, guess_belongs_to_game):
    # arrange
    response = client.get(f"/games/{new_game_without_id.game_id}/guesses")
    response_body = response.get_json()

    # assert
    assert response.status_code == 200
    assert len(response_body) == 1
    assert response_body == [
        {"guess": "1111", "game_id": 1, "correct_num": None, "correct_loc": None, "guess_id": 1}]
