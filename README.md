# AOC Utilities

This is a little python utility package to help with my [Advent of Code challenges](https://github.com/loganmeetsworld/advent-of-code).

## Setup

To use, first install:

```bash
pip3 install aoc_utils
```

Then you will also need a session cookie setup. You can find your session cookie by logging into adventofcode.com and inspecting your session with developer tools. You'll need to set this in the environment. I do this with a script that contains the following:

```bash
export SESSION_COOKIE="cookie"
```

Once you have the module installed and the session cookie set you can use by importing like:

```python
from aoc_utils import aoc_utils
```

Current it is just one module for the package. One you have it there are several functions available.

We can fetch our input or our problem within a folder like so:

```python
year = 2019
day = 1
problem_input = aoc_utils.fetch(year, day, 'input|problem')
```

We can also save to a path like:

```python
year = 2019
day = 1
problem_input = aoc_utils.save('/Path/To/Save', year, day, 'input|problem')
```

We can submit answers to AOC via an `answer()` function that takes the input and part we are working on.

```python
year = 2019
day = 1
level = 1

def answer(level, input):
    print('solve puzzle')

aoc_utils.submit(year, day, level, answer)
```

We can also test with test cases that look like this:

```python
test_cases = [
  ['<level>', '<correct_answer>', '<submitted_answer>']
]
```

and then test and submit like:

```python
year = 2019
day = 1
test_cases = [
  ['<level>', '<correct_answer>', '<submitted_answer>']
]
def answer(level, input):
    print('solve puzzle')

aoc_utils.test_and_submit(year, day, test_cases, answer)
```
