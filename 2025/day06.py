import itertools as it
from functools import reduce
from operator import mul, add
from typing import Iterable

with open(f'{__file__.split(".")[0]}.txt', mode="r") as f:
    # Leading and trailing spaces matter in this challenge, so do not strip() lines here
    input_lines = [l for l in f.readlines()]


def split_line(line: str) -> tuple[str, ...]:
    return tuple(s for s in line.split() if s)


def solve_problem(inputs: Iterable[str | int | float], op_str: str) -> int:
    operators = {
        "+": add,
        "*": mul,
    }
    inputs = list(inputs)
    return reduce(operators[op_str], map(int, inputs))


def line_to_padded_nums(line: str, col_starts: Iterable[int], col_lens: Iterable[int]) -> tuple[str, ...]:
    idx_len_pairs = zip(col_starts, col_lens)
    return tuple(line[i:i + width] for i, width in idx_len_pairs)


def read_col_vertically(col_nums: Iterable[str]) -> Iterable[int]:
    # Go through the numbers (as strings) in the column and read them character by character (all first chars, ...)
    # Joining them together the character into a string and converting to int yields the final number in that column.
    # IMPORTANT: There may be spaces, which typically can be read as zeroes. However, leading and trailing zeroes
    #            should not be considered (see numbers of second column in the input, which are "6883", "746", "97").
    #            This is why the chars are stripped before converting to int.
    return (int("".join(col_chars).strip()) for col_chars in zip(*col_nums))


if __name__ == "__main__":
    num_lines = input_lines[:-1]
    op_line = input_lines[-1]

    # Part 1
    segmented_lines = (split_line(line) for line in input_lines)
    input_cols = list(zip(*segmented_lines))
    results = [solve_problem(col[:-1], col[-1]) for col in input_cols]
    print(f"Part 1: {sum(results)}")

    # Part 2
    col_idxs = tuple(i for i, char in enumerate(op_line) if char in "+*")
    operators = op_line.replace(" ", "")
    max_line_length = max(len(line) for line in num_lines)
    col_idxs_with_end = it.chain(col_idxs, [max_line_length])
    # Width of each column is the distance between operators minus 1 (for space separator)
    col_widths = tuple(j - i - 1 for i, j in it.pairwise(col_idxs_with_end))

    # Parse and convert the lines into slices lines, columns, and then into numbers for each column - step by step.
    padded_lines = [line_to_padded_nums(line, col_idxs, col_widths) for line in num_lines]
    padded_cols = list(zip(*padded_lines))
    parsed_cols = [list(read_col_vertically(col)) for col in padded_cols]

    results_part2 = [solve_problem(col_nums, op) for col_nums, op in zip(parsed_cols, operators)]
    print(f"Part 2: {sum(results_part2)}")
