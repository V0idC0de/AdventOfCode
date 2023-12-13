import itertools
import timeit
from functools import lru_cache


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]
    line_iter = iter(input_lines)
    blocks = []
    while block := list(itertools.takewhile(lambda row: len(row), line_iter)):
        blocks.append(block)

    # Part 1
    block_scores = [get_block_score(block) for block in blocks]
    print(f"Challenge 1: {sum(block_scores)}")


def get_block_score(block: list[str]) -> int:
    # Try vertical mirror, then transpose the block and try again (looking for horizontal mirrors).
    vertical = find_mirror(block)
    horizontal = None
    if vertical is None:
        horizontal = find_mirror(["".join(rows) for rows in zip(*block)])
    return vertical if vertical is not None else horizontal * 100


def find_mirror(block: list[str]) -> int | None:
    """ Tests `block` for vertical mirrors and returns the index of the mirror (the amount of columns left to it). """
    # For this puzzle, it's safe to assume all lines are of equal length
    row_length = len(block[0])
    for i in range(1, row_length):
        # Find the shorter side
        min_side_length = min(i, row_length - i)
        if all(is_mirrored(row[i - min_side_length:i + min_side_length]) for row in block):
            return i
    # No mirrors found
    return None


@lru_cache
def is_mirrored(line: str) -> bool:
    return line[:len(line) // 2] == "".join(reversed(line[len(line) // 2:]))


if __name__ == '__main__':
    main()
