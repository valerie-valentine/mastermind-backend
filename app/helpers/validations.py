from flask import abort, make_response
from sqlalchemy.inspection import inspect
from app.models.client import Client
from app import bcrypt
from ..db import db


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    # Dynamically finds the primary key column for the model
    primary_key_column = inspect(cls).primary_key[0].name

    query = db.select(cls).where(getattr(cls, primary_key_column) == model_id)
    model = db.session.scalar(query)

    # query = db.select(cls).where(cls.id == model_id)
    # model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model


def validate_guess_data(game_data, guess):
    if game_data.lives == 0:
        abort(make_response({"details": f"Guess: {
              guess} invalid. Lives have been exceeded. No more guesses allowed."}, 400))
    if not isinstance(guess, str) or not guess.isdigit():
        abort(make_response({"details": f"Guess: {
              guess} invalid. Guess must be an numerical value of type string"}, 400))
    if len(guess) != game_data.difficulty_level:
        abort(make_response({"details": f"Guess: {guess} invalid. Guess must be {
              game_data.difficulty_level} digits long"}, 400))

    for num in guess:
        int_num = int(num)
        if int_num not in range(game_data.num_min, game_data.num_max + 1):
            abort(make_response({"details": f"Guess: {guess} invalid. Each digit in the guess must be between the range of {
                  game_data.num_min} and {game_data.num_max}"}, 400))

    for saved_guess in game_data.guesses:
        if guess == saved_guess.guess:
            abort(make_response({"details": f"Guess: {
                guess} invalid. Guess has been played previously"}, 400))

    return guess


def validate_game_data(request_data):
    if "lives" in request_data:
        if not isinstance(request_data["lives"], int) or int(request_data["lives"]) > 20 or int(request_data["lives"]) < 3:
            abort(make_response(
                {"details": f"Invalid Choice: Please enter a numerical value for lives between 3 and 20"}, 400))
    if "num_min" in request_data:
        if not isinstance(request_data["num_min"], int) or request_data["num_min"] < 0:
            abort(make_response(
                {"details": f"Invalid Choice: Please enter a numerical value for num_min greater than or equal to 0 and less than 9"}, 400))
    if "num_max" in request_data:
        if not isinstance(request_data["num_max"], int) or int(request_data["num_max"]) >= 10 or int(request_data["num_min"]) >= int(request_data["num_max"]):
            abort(make_response(
                {"details": f"Invalid choice: Please enter a numerical value less than equal to 9 and larger than num_min: {request_data["num_min"]} "}, 400))
    if "difficulty_level" in request_data:
        if not request_data["difficulty_level"] in [4, 6, 8]:
            abort(make_response(
                {"details": f"Invalid choice: Please enter a valid level: easy, medium, hard"}, 400))

    return request_data


def validate_client_data(client_data):
    email = client_data.get("email")
    password = client_data.get("password")

    if not email or not password:
        abort(make_response(
            {'details': 'Failed to create client. Email and password are required.'}, 400))
    if not isinstance(email, str) or not isinstance(password, str):
        abort(make_response(
            {'details': 'Failed to create client. Invalid datatype for email or password'}, 400))

    existing_client = Client.query.filter_by(email=email).first()

    if existing_client:
        abort(make_response({'details': f'Email "{
              email}" already exists. Please choose another email.'}, 400))

    return client_data


def validate_client_login(request_data):
    email = request_data.get("email")
    password = request_data.get("password")

    if not email or not password:
        abort(make_response(
            {'details': 'Failed login. Email and password are required.'}, 400))
    if not isinstance(email, str) or not isinstance(password, str):
        abort(make_response(
            {'details': 'Falied login. Please enter valid email or password'}, 400))

    client = Client.query.filter_by(email=email).first()
    if not client or not bcrypt.check_password_hash(client.password, password):
        abort(make_response(
            {'details': 'Failed login: Please check your login credentials'}, 404))

    return client
