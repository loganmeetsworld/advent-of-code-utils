from bs4 import BeautifulSoup
from colorama import Fore, Style
import os
import requests

CURRENT_DIR = os.getcwd()
HEADERS = {"cookie": f"session={os.environ['SESSION_COOKIE']}", }


def request_content(year, day, content_type):
    if content_type == 'input':
        url = f"https://adventofcode.com/{year}/day/{day}/input"
    elif content_type == 'problem':
        url = f"https://adventofcode.com/{year}/day/{day}"

    response = requests.get(url, headers=HEADERS)
    handle_error_status(response.status_code)
    return response.text.strip()


def fetch(year, day, content_type):
    content = request_content(year, day, content_type)
    if content_type == 'input':
        return content
    elif content_type == 'problem':
        soup = BeautifulSoup(content, "html.parser")
        return '\n\n\n'.join([a.text for a in soup.select('article')])


def save(path_to_save, year, day, content_type):
    content = fetch(year, day, content_type)
    with open(f"{path_to_save}/{content_type}.txt", "w") as text_file:
        text_file.write(content)

    return content


def fetch_and_save(year, day):
    if os.path.exists(f"{CURRENT_DIR}/input.txt"):
        print("Found input locally, using saved input...\n")
        with open(f"{CURRENT_DIR}/input.txt") as file:
            return file.read()
    else:
        print("Input not found, fetching...\n")
        problem_text = save(CURRENT_DIR, year, day, content_type="problem")
        print(f"\n{problem_text}\n")
        return save(CURRENT_DIR, year, day, content_type="input")


def detect_time():
    return [CURRENT_DIR.split('/')[-2], CURRENT_DIR.split('/')[-1].split('-')[1]]


def submit(year, day, level, answer):
    print(f"\nFor Day {day}, Part {level}, we are submitting answer: {answer}\n")
    data = {"level": str(level), "answer": str(answer)}
    response = requests.post(f"https://adventofcode.com/{year}/day/{day}/answer", headers=HEADERS, data=data)
    soup = BeautifulSoup(response.text, "html.parser")
    message = soup.article.text

    if "that's the right answer" in message.lower():
        print(f"\n{Fore.GREEN}Correct! ⭐️{Style.RESET_ALL}")
        star_path = os.getcwd()
        with open(f"{star_path}/stars.txt", "w+") as text_file:
            print("Writing '*' to star file...")
            text_file.write('*')
            if level == 1:
                print("Updated problem with part 2:\n\n")
                print(save(CURRENT_DIR, year, day, 'problem'))
    elif "not the right answer" in message.lower():
        print(f"\n{Fore.RED}Wrong answer! For details:\n{Style.RESET_ALL}")
        print(message)
    elif "answer too recently" in message.lower():
        print(f"\n{Fore.YELLOW}You gave an answer too recently{Style.RESET_ALL}")


def test(answer, cases):
    all_passed = True

    for tc in cases:
        submitted_answer = answer(tc['input'], tc['level'])
        if str(tc['output']) == str(submitted_answer):
            print(f"{Fore.GREEN}Test passed 🥳 {Style.RESET_ALL} Part {tc['level']}; Input: '{tc['input']}'; Output: '{tc['output']}'")
        else:
            all_passed = False
            print(f"{Fore.RED}Test failed ☹️ {Style.RESET_ALL} Part {tc['level']}; Input: '{tc['input']}'; Submitted: '{submitted_answer}'; Correct: '{tc['output']}'")

    return all_passed


def check_stars():
    star_path = os.getcwd()
    star_file = f"{star_path}/stars.txt"
    if os.path.exists(star_file):
        with open(star_file, 'r') as file:
            stars = file.read().strip()
            return len(stars)


def handle_error_status(code):
    if code == 404:
        print(f"{Fore.RED}{code}: This day is not available yet!{Style.RESET_ALL}")
        quit()
    elif code == 400:
        print(f"{Fore.RED}{code}: Bad credentials!{Style.RESET_ALL}")
        quit()
    elif code > 400:
        print(f"{Fore.RED}{code}: General error!{Style.RESET_ALL}")
        quit()


def run(answer_func, test_cases, year=None, day=None):
    if not year and not day:
        year, day = detect_time()

    problem_input = fetch_and_save(year, day)

    if test(answer_func, test_cases):
        print("\nCongratulations! All tests passed. Now looking to submit your answers...\n")
        stars = check_stars()
        if not stars:
            answer = answer_func(problem_input, 1)
            print("You are submitting your answer to part 1 of this puzzle. Do you want to submit? P1: {answer}\n")
            submit_answer = input()
            if submit_answer == 'y':
                submit(year, day, answer, level=1)
        elif stars == 1:
            answer = answer_func(problem_input, 2)
            print("It seems we'e been here before and you've submitted one answer ⭐️ Are you sure you want to submit part 2? P2: {answer}\n")
            submit_answer = input()
            if submit_answer == 'y':
                submit(year, day, answer, level=2)
        else:
            print("It seems we've been here before and you've submitted both answers! ⭐️⭐️\n")
