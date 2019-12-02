# AOC Utilities

This is a little python utility package to help with my [Advent of Code challenges](https://github.com/loganmeetsworld/advent-of-code).

## Setup

To use, first install:

```bash
git clone git@github.com:loganmeetsworld/aoc_utils.git
cd aoc_utils
pip3 install .
```

Then you will also need a session cookie setup. You can find your session cookie by logging into adventofcode.com and inspecting your session with developer tools. You'll need to set this in the environment. I do this with a script that contains the following:

```bash
export SESSION_COOKIE="cookie"
```

Once you have the module installed and the session cookie set you can use by importing like:

```python
from aoc_utils import aoc_utils
```

Current it is just one module for the package. One you have it there are several functions available. The package assumes you are in a current directory of the problem you are trying to solve. The `run` method allows you to enter the year and day if you want to specify. For me, I have all my problems formatted `advent_of_code/2019/day-1` which allows me to guess the year and day.

We can fetch our input or our problem within a folder like so:

```python
year = 2019
day = 1
problem_input = aoc_utils.fetch_and_save('input|problem', year=year, day=day)
```

This will fetch the input.txt and problem.txt if they do not exist, otherwise will fetch the problem_input from a saved input.txt file.

We can submit answers to AOC via an `answer()` function that takes the input and part we are working on.

```python
year = 2019
day = 1
level = 1

def answer(level, input):
    print('solve puzzle')

aoc_utils.submit(level, answer, year=year, day=day)
```

We can also test with test cases that look like this:

```python
test_cases = [
  {'level': 1, 'input': '12', 'output': '100'}
]
```

and test like this:

```python
test_cases = [
  {'level': 1, 'input': '12', 'output': '100'}
]
def answer(level, input):
    print('solve puzzle')

# Test returns a bool
passed_all = aoc_utils.test(answer, test_cases)
```

and then finally, when you put it all together, you simply use `run()` which will pull input, test based on a list of cases, and then attempt to submit answers.

```python
year = 2019
day = 1
test_cases = [
  {'level': 1, 'input': '12', 'output': '100'}
]
def answer(level, input):
    print('solve puzzle')

aoc_utils.run(answer, test_cases=test_cases, year=year, day=day)
```

We keep state of what questions we've gotten right in a a `stars.txt` file created for correct answers. Test cases are optional. If there are no tests, it will move to submit.
