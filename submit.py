import requests
import os
import bs4

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

    soup = bs4.BeautifulSoup(response.text, "html.parser")
    message = soup.article.text

    if "That's the right answer" in message:
        print("Correct!")
    elif "That's not the right answer" in message:
        print("Wrong answer!")
    elif "You gave an answer too recently" in message:
        print("Wait a bit, too recent a answer...")
