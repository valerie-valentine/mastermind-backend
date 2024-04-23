from flask import abort, make_response
import requests
import os
import requests


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response(
            {"details": f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response(
            {"details": f"{cls.__name__} {model_id} not found"}, 404))

    return model


def random_number(digits):
    url = f'https://www.random.org/integers/?num={
        digits}&min=0&max=9&col=1&base=10&format=plain&rnd=new'

    response = requests.get(url)

    random_number = "".join(response.text.split())
    return random_number


def check_user_guess(game_data, guess):
    correct_number = 0
    correct_location = 0
    answer_count = {}

    for num in game_data.answer:
        answer_count[num] = answer_count.get(num, 0) + 1

    for i, num in enumerate(guess):
        if num == game_data.answer[i]:
            correct_location += 1
        if num in answer_count and answer_count[num] > 0:
            correct_number += 1
            answer_count[num] -= 1

    if guess == game_data.answer:
        game_data.game_status = "Win"
    else:
        game_data.lives -= 1
        if game_data.lives == 0:
            game_data.game_status = "Loss"

    return correct_number, correct_location


def validate_user_guess(game_data, guess):
    if game_data.lives == 0:
        abort(make_response({"details": f"Guess: {
              guess} invalid. Lives have been exceeded. No more guesses allowed."}, 400))
    if not guess.isnumeric():
        abort(make_response({"details": f"Guess: {
              guess} invalid. Guess must be an numerical value"}, 400))
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
    # Should i have a check to for key 1st or not?
    if "lives" in request_data:
        if not isinstance(request_data["lives"], int) or int(request_data["lives"]) >= 20 or int(request_data["lives"]) < 3:
            abort(make_response(
                {"details": f"Invalid Choice: Please enter a numerical value for lives between 3 and 20"}, 400))
    if "num_min" in request_data:
        if not isinstance(request_data["num_min"], int) or request_data["num_min"] < 0:
            abort(make_response(
                {"details": f"Invalid Choice: Please enter a numerical value for num_min greater than or equal to 0 and less than 9"}, 400))
    if "num_max" in request_data:
        if not isinstance(request_data["num_max"], int) or int(request_data["num_max"]) >= 9 or int(request_data["num_min"]) >= int(request_data["num_max"]):
            abort(make_response(
                {"details": f"Invalid choice: Please enter a numerical value less than equal to 9 and larger than num_min: {request_data["num_min"]} "}, 400))
    if "difficulty_level" in request_data:
        if not request_data["difficulty_level"] in [4, 6, 8]:
            abort(make_response(
                {"details": f"Invalid choice: Please enter a valid level: easy, medium, hard"}, 400))

    return request_data


def generate_hint(game_data):
    guess = [guess.to_dict() for guess in game_data.guesses][-1]
    answer = game_data.answer

    if int((guess["guess"])) < int(answer):
        return {'hint': f"The answer if greater than your last guess {guess["guess"]}"}
    else:
        return {'hint': f"The answer if less than your last guess {guess["guess"]}"}
