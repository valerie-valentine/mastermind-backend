import requests


def random_number(digits, num_min, num_max):
    url = f'https://www.random.org/integers/?num={
        digits}&min={num_min}&max={num_max}&col=1&base=10&format=plain&rnd=new'

    response = requests.get(url)

    # result digits are new line separated, join them to get a single string
    random_number = "".join(response.text.split())
    return random_number
