import operator
import string
from functools import reduce
from typing import Tuple, Set, List

with open(f'{__file__.split(".")[0]}.txt') as f:
    lines = [l.strip() for l in f.readlines()]


def split_line(s: str) -> Tuple[str, str]:
    return s[:len(s) // 2], s[len(s) // 2:]


def find_duplicates(str_tuple: Tuple[str, str]) -> set:
    s1, s2 = str_tuple
    return set(s1) & set(s2)


def letter_to_score(s: set) -> int:
    alphabet = string.ascii_lowercase + string.ascii_uppercase
    return alphabet.index(s.pop()) + 1


lines_map = sum(map(letter_to_score,
                    map(find_duplicates,
                        map(split_line, lines))))

print(f"Part 1: {lines_map}")

lines_as_sets: List[Set] = [set(l) for l in lines]
groups: List[List[Set]] = [lines_as_sets[i:i+3] for i in range(0, len(lines_as_sets), 3)]
unique_letters = [reduce(operator.and_, group) for group in groups]
print(f"Part 2: {sum(letter_to_score(s) for s in unique_letters)}")
