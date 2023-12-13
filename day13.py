import itertools
import timeit
from functools import lru_cache
from typing import Callable


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]
    line_iter = iter(input_lines)
    blocks = []
    while block := list(itertools.takewhile(lambda row: len(row), line_iter)):
        blocks.append(block)

    # Part 1
    block_scores = [get_block_score(block, find_mirror) for block in blocks]
    print(f"Challenge 1: {sum(block_scores)}")

    # Part 2
    block_scores = [get_block_score(block, find_mirror_off_by_one) for block in blocks]
    print(f"Challenge 2: {sum(block_scores)}")


def get_block_score(block: list[str], mirror_finder: Callable[[list[str]], int | None]) -> int:
    # Try vertical mirror, then transpose the block and try again (looking for horizontal mirrors).
    vertical = mirror_finder(block)
    horizontal = None
    if vertical is None:
        horizontal = mirror_finder(["".join(rows) for rows in zip(*block)])
    return vertical if vertical is not None else horizontal * 100


def find_mirror(block: list[str]) -> int | None:
    """ Tests `block` for vertical mirrors and returns the index of the mirror (the amount of columns left to it). """
    # For this puzzle, it's safe to assume all lines are of equal length
    row_length = len(block[0])
    for i in range(1, row_length):
        # Find the shorter side
        min_side_length = min(i, row_length - i)
        if all(mirror_diffs(row[i - min_side_length:i + min_side_length]) == 0 for row in block):
            return i
    # No mirrors found
    return None


def find_mirror_off_by_one(block: list[str]) -> int | None:
    """
    Works like `find_mirror()` but finds a mirror location where there's exactly one character,
    which is not perfectly mirrored.
    """
    row_length = len(block[0])
    for i in range(1, row_length):
        # Find the shorter side
        min_side_length = min(i, row_length - i)
        if sum(mirror_diffs(row[i - min_side_length:i + min_side_length]) for row in block) == 1:
            return i
    # No mirrors found
    return None


@lru_cache
def mirror_diffs(line: str) -> int:
    """
    Checks whether `line` is a palindrome and return the amount of character pairs, which do NOT match.

    :param line: Iterable with EVEN length (odd length will never return `0`).
    :return: Amount of differing character pairs
    """
    line_chars_pairwise = zip(line[:len(line) // 2], reversed(line[len(line) // 2:]))
    return sum(1 for c1, c2 in line_chars_pairwise if c1 != c2)


if __name__ == '__main__':
    main()
