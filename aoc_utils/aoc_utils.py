from bs4 import BeautifulSoup
import os
import requests


def fetch(path, content_type):
    year = path.split("/")[-3]
    day = path.split("/")[-2].split("-")[1]
    headers = {"cookie": f"session={os.environ['SESSION_COOKIE']}",}
    if content_type == 'input':
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", headers=headers)
        _handle_error(response.status_code)
        message = response.text.strip()
    elif content_type == 'problem':
        response = requests.get(f"https://adventofcode.com/{year}/day/{day}", headers=headers)
        _handle_error(response.status_code)
        soup = BeautifulSoup(response.text, "html.parser")
        message = soup.article.text

    return message


def save(path, content_type):
    content = fetch(path, content_type)
    save_path = "/".join(path.split("/")[0:-1])
    with open(f"{save_path}/{content_type}.txt", "w") as text_file:
        text_file.write(content)


def submit(path, level, answer):
    year = path.split("/")[-3]
    day = path.split("/")[-2].split("-")[1]

    print(f"For Day {day}, Part {level}, we are submitting answer: {answer}")

    headers = {"cookie": f"session={os.environ['SESSION_COOKIE']}",}
    data = {
        "level": str(level),
        "answer": str(answer)
    }

    response = requests.post(f"https://adventofcode.com/{year}/day/{day}/answer", headers=headers, data=data)

    soup = BeautifulSoup(response.text, "html.parser")
    message = soup.article.text

    if "That's the right answer" in message:
        print("Correct!")
        star_path = "/".join(path.split("/")[0:-1])
        with open(f"{star_path}/stars.txt", "w+") as text_file:
            print("Writing '*' to star file...")
            text_file.write('*')

    elif "That's not the right answer" in message:
        print("Wrong answer!")
    elif "You gave an answer too recently" in message:
        print("Wait a bit, too recent a answer...")


def test(test_cases, answer):
    passed = True
    for test_case in test_cases:
        problem_input = test_case[1]
        submitted_answer = answer(problem_input, test_case[0])
        real_answer = test_case[2]
        if str(real_answer) == str(submitted_answer):
            print(f"Test passed! for input {real_answer}")
        else:
            passed = False
            print(f"Test failed :( for input {problem_input}, you put {submitted_answer}, correct: {real_answer}")

    if passed:
        return 'passed'


def check_stars(path):
    star_path = "/".join(path.split("/")[0:-1])
    star_file = f"{star_path}/stars.txt"
    if os.path.exists(star_file):
        with open(star_file, 'r') as file:
            stars = file.read().strip()
            return len(stars)


def test_and_submit(path, test_cases, problem_input, answer):
    test_results = test(test_cases, answer)

    if test_results == 'passed':
        print("\nCongratulations! All tests passed.")
        stars = check_stars(os.path.abspath(__file__))
        if stars and stars < 2:
            print('Would you like to submit this answer? y/n')
        else:
            print("It seems we've been here before and you've submitted both answers!")

        if stars == 0:
            print(f'Part 1: {answer(problem_input, 1)}')
            submit_answer = input()
            if submit_answer == 'y':
                submit(os.path.abspath(__file__), 1, answer(problem_input, 1))

        elif stars == 1:
            print(f'Part 2: {answer(problem_input, 2)}')
            submit_answer = input()
            if submit_answer == 'y':
                submit(os.path.abspath(__file__), 2, answer(problem_input, 2))


def _handle_error(code):
    if code == 404:
        raise ValueError("This day is not available yet!")
    elif code == 400:
        raise ValueError("Bad credentials!")
