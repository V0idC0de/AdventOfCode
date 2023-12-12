import itertools
import re
from collections.abc import Iterable
from typing import Generator


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]
    lines = [line.split() for line in input_lines]

    # Part 1
    possibilities_per_line = ((possible_patterns(line), pattern_to_regex(pattern)) for line, pattern in lines)
    options_per_line = (count_valid_patterns(s, regex) for s, regex in possibilities_per_line)
    print(f"Challenge 1: {sum(options_per_line)}")


def possible_patterns(line: str) -> Generator:
    """ Generates all possible variants of `line` replacing each `?` with either `.` or `#`. """
    replacement_chars = [".", "#"]
    char_possibilities = ((replacement_chars if char == "?" else [char]) for char in line)
    return ("".join(chars) for chars in itertools.product(*char_possibilities))


def pattern_to_regex(pattern: str | tuple[int, ...]) -> re.Pattern:
    if isinstance(pattern, str):
        pattern = tuple(pattern.strip().split(","))
    # Build one '#{x}' per number in pattern, which indicates the amount subsequent #-characters.
    # Separate them with at least 1 dot using "\.+" and set any amount of dots before and after the regex with "\.*".
    regex_str = r"^\.*" + r"\.+".join(f'#{{{amount}}}' for amount in pattern) + r"\.*$"
    return re.compile(regex_str)


def count_valid_patterns(lines: Iterable[str], regex: re.Pattern) -> int:
    return sum(1 for line in lines if regex.match(line))


if __name__ == '__main__':
    main()
