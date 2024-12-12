from flask import abort, make_response
import os
import requests
from app.models.client import Client
from app import bcrypt
from .db import db

# old way validate_model w/o query building


# def validate_model(cls, model_id):
#     try:
#         model_id = int(model_id)
#     except:
#         abort(make_response(
#             {"details": f"{cls.__name__} {model_id} invalid"}, 400))

#     model = cls.query.get(model_id)

#     if not model:
#         abort(make_response(
#             {"details": f"{cls.__name__} {model_id} not found"}, 404))

#     return model


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)

    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict(), 201


def random_number(digits, num_min, num_max):
    url = f'https://www.random.org/integers/?num={
        digits}&min={num_min}&max={num_max}&col=1&base=10&format=plain&rnd=new'

    response = requests.get(url)

    # result digits are new line separated, join them to get a single string
    random_number = "".join(response.text.split())
    return random_number


# def check_client_guess(game_data, guess, client):
#     correct_number = 0
#     correct_location = 0
#     answer_count = {}

#     for num in game_data.answer:
#         answer_count[num] = answer_count.get(num, 0) + 1

#     for i, num in enumerate(guess):
#         if num == game_data.answer[i]:
#             correct_location += 1
#         if num in answer_count and answer_count[num] > 0:
#             correct_number += 1
#             answer_count[num] -= 1

    # if guess == game_data.answer:
    #     game_data.game_status = "Win"
    #     if client:
    #         client.score += 1
    # else:
    #     game_data.lives -= 1
    #     if game_data.lives == 0:
    #         game_data.game_status = "Loss"

#     return correct_number, correct_location

def check_client_guess(game_data, guess_data):
    correct_number = 0
    correct_location = 0
    answer_count = {}

    for num in game_data.answer:
        answer_count[num] = answer_count.get(num, 0) + 1

    for i, num in enumerate(guess_data):
        if num == game_data.answer[i]:
            correct_location += 1
        if num in answer_count and answer_count[num] > 0:
            correct_number += 1
            answer_count[num] -= 1

    # if guess == game_data.answer:
    #     game_data.game_status = "Win"
    #     if client:
    #         client.score += 1
    # else:
    #     game_data.lives -= 1
    #     if game_data.lives == 0:
    #         game_data.game_status = "Loss"

    return correct_number, correct_location


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


def generate_hint(game_data):
    # can probably just do game_data.guesses[-1]
    # guess = [guess.to_dict() for guess in game_data.guesses][-1]
    last_guess = game_data.guesses[-1].to_dict()
    answer = game_data.answer

    if int((last_guess["guess"])) < int(answer):
        return {'hint': f"The answer is greater than your last guess {last_guess["guess"]}"}
    else:
        return {'hint': f"The answer is less than your last guess {last_guess["guess"]}"}


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
