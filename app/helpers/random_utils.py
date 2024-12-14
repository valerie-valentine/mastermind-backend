import requests
from flask import abort, make_response


def random_number_api(digits, num_min, num_max):
    url = f'https://www.random.org/integers/?num={digits}&min={
        num_min}&max={num_max}&col=1&base=10&format=plain&rnd=new'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            random_number = "".join(response.text.split())
            return random_number
        else:
            response = {"details": f"Random generator API failed with status code: {
                response.status_code}"}
            abort(make_response(response, 503))
    except requests.exceptions.RequestException as e:
        response = {
            "details": f"Error occurred while connecting to the API: {e}"}
        abort(make_response(response, 503))
