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


def save(year, day, content_type):
    content = fetch(year, day, content_type)
    with open(f"{CURRENT_DIR}/{content_type}.txt", "w") as text_file:
        text_file.write(content)

    return content


def fetch_and_save(year, day):
    if os.path.exists(f"{CURRENT_DIR}/input.txt"):
        print("\n🛷  Found input locally, using saved input 🛷 \n")
        with open(f"{CURRENT_DIR}/input.txt") as file:
            return file.read()
    else:
        print("\n🛷  Input not found, fetching 🛷 \n")
        problem_text = save(year, day, content_type="problem")
        print(f"\n{problem_text}\n")
        return save(year, day, content_type="input")


def submit(answer, level, year, day):
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
                print(save(year, day, 'problem'))
    elif "not the right answer" in message.lower():
        print(f"\n{Fore.RED}Wrong answer 🎅🏾🙅🏼‍♀️! For details:\n{Style.RESET_ALL}")
        print(message)
    elif "answer too recently" in message.lower():
        print(f"\n{Fore.YELLOW}You gave an answer too recently{Style.RESET_ALL}")
    elif "already complete it" in message.lower():
        print(f"\n{Fore.YELLOW}You have already solved this. Make sure a local stars.txt file is present that reflects your stars for this problem.{Style.RESET_ALL}")


def test(answer_func, cases):
    all_passed = True

    if not cases:
        print("Livin' on the edge! No test cases defined.")
        return all_passed

    for tc in cases:
        answer = answer_func(tc['input'], tc['level'], test=True)
        if str(tc['output']) == str(answer):
            print(f"{Fore.GREEN}🎄 Test passed {Style.RESET_ALL}[Part {tc['level']}] Input: '{tc['input']}'; Output: '{tc['output']}'")
        else:
            all_passed = False
            print(f"{Fore.RED}🔥 Test failed {Style.RESET_ALL}[Part {tc['level']}] Input: '{tc['input']}'; Submitted: '{answer}'; Correct: '{tc['output']}'")

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


def run(answer_func, test_cases=None, year=None, day=None):
    if not year and not day:
        year, day = CURRENT_DIR.split('/')[-2:]

    problem_input = fetch_and_save(year, day)

    if test(answer_func, test_cases):
        print("\n🍾 Now looking to submit your answers 🍾\n")
        stars = check_stars()
        if not stars:
            level = 1
            answer = answer_func(problem_input, level)
            print(f"🙇‍♀️ You are submitting your answer to part 1 of this puzzle. \nDo you want to submit part 1 (y/n)? P1: {answer}")
            submit_answer = input()
            if submit_answer == 'y':
                submit(answer, level, year, day)
        elif stars == 1:
            level = 2
            answer = answer_func(problem_input, level)
            print(f"👯‍♀️  It seems we've been here before and you've submitted one answer ⭐️ \nDo you want to submit part 2 (y/n)? P2: {answer}")
            submit_answer = input()
            if submit_answer == 'y':
                submit(answer, level, year, day)
        else:
            print("It seems we've been here before and you've submitted both answers! ⭐️⭐️\n")
    else:
        print("\n🤷‍♀️ You know the rules. Tests don't pass, YOU don't pass.\n")
