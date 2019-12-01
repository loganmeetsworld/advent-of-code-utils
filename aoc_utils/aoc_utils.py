from bs4 import BeautifulSoup
from colorama import Fore, Style
import os
import requests


def fetch(year, day, content_type):
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


def save(path_to_save, year, day, content_type):
    content = fetch(year, day, content_type)
    with open(f"{path_to_save}/{content_type}.txt", "w") as text_file:
        text_file.write(content)
    
    return content


def detect_time():
    c = os.getcwd()

    return [c.split('/')[-2], c.split('/')[-1].split('-')[1]]


def submit(year, day, level, answer):
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
        print("Correct! ⭐️")
        star_path = os.getcwd()
        with open(f"{star_path}/stars.txt", "w+") as text_file:
            print("Writing '*' to star file...")
            text_file.write('*')
    elif "That's not the right answer" in message:
        print("Wrong answer! For details:\n")
        print(message)
    elif "You gave an answer too recently" in message:
        print("Wait a bit, too recent a answer...")


def test(test_cases, answer):
    passed = True
    for test_case in test_cases:
        submitted_answer = answer(test_case['input'], test_case['level'])
        if str(test_case['output']) == str(submitted_answer):
            print(f"{Fore.GREEN}Test passed for part {test_case['level']}! for input {test_case['output']}{Style.RESET_ALL}")
        else:
            passed = False
            print(f"{Fore.RED}Test failed :( for input {test_case['input']}, you put {submitted_answer}, correct: {test_case['output']}{Style.RESET_ALL}")

    if passed:
        return 'passed'


def fetch_and_save(year, day):
    current_dir = os.curdir
    if os.path.exists(f'{current_dir}/input.txt'):
        print('Found input already, using saved input...\n')
        with open(f'{current_dir}/input.txt') as file:
            problem_input = file.read()
    else:
        print('Input not found, fetching...\n')
        problem_input = save(current_dir, 2019, 1, 'input')
        save(current_dir, 2019, 1, 'problem')
    
    return problem_input


def check_stars():
    star_path = os.getcwd()
    star_file = f"{star_path}/stars.txt"
    if os.path.exists(star_file):
        with open(star_file, 'r') as file:
            stars = file.read().strip()
            return len(stars)


def test_and_submit(year, day, test_cases, problem_input, answer):
    test_results = test(test_cases, answer)

    if test_results == 'passed':
        print("\nCongratulations! All tests passed.")
        stars = check_stars()
        if stars and stars < 2:
            print('Would you like to submit this answer? y/n')
        else:
            print("It seems we've been here before and you've submitted both answers!")

        if stars == 0:
            print(f'Part 1: {answer(problem_input, 1)}')
            submit_answer = input()
            if submit_answer == 'y':
                submit(year, day, 1, answer(problem_input, 1))

        elif stars == 1:
            print(f'Part 2: {answer(problem_input, 2)}')
            submit_answer = input()
            if submit_answer == 'y':
                submit(year, day, 2, answer(problem_input, 2))


def _handle_error(code):
    if code == 404:
        raise ValueError("This day is not available yet!")
    elif code == 400:
        raise ValueError("Bad credentials!")
