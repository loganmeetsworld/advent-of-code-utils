from bs4 import BeautifulSoup
import os
import requests


def fetch(path, content_type):
    year = path.split("/")[-3]
    day = path.split("/")[-2].split("-")[1]
    headers = {"cookie": f"session={os.environ['SESSION_COOKIE']}",}
    if content_type == 'input':
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", headers=headers)
        handle_error(response.status_code)
        message = response.text.strip()
    elif content_type == 'problem':
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}", headers=headers)
        handle_error(response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")
        message = soup.article.text

    return message


def save(path, content_type):
    content = fetch(path, content_type)
    with open(f"{path}/{content_type}.txt", "w") as text_file:
        text_file.write(content)


def handle_error(code):
    if code == 404:
        raise "This day is not available yet!"
    elif code == 400:
        raise "Bad credentials!"
