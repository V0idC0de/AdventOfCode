with open(f'{__file__.split(".")[0]}.txt') as f:
    input_lines = [l.strip() for l in f.readlines()]

import re
from collections import namedtuple

Coords = namedtuple("Coords", "line start end")


def is_symbol_around(lines: list[str], pos: Coords) -> bool:
    """
    Determines whether any symbol not listed in `non_symbol_chars` is in adjacent coordinates of `pos`.
    Diagonal is considered adjacent.

    :param lines: Lines of text, in which `pos` is a location
    :param pos: Position within the char-grid `lines` to check. Declares line number and an index-range in the line.
    :return: Whether a symbol not listed in `non_symbol_chars` is adjacent to `pos` in `lines`.
    """
    line_len = len(lines[0])
    non_symbol_chars = [".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    # Calculate the index for the column before and after the string, while considering boundaries
    # after_idx is not increased, as it's the index. Using it as slice-index later requires a +1 since
    # slicing is exclusive with the end-index. Due to this however, the limit is decreased by 1 to not overrun the line.
    before_idx, after_idx = max(pos.start - 1, 0), min(pos.end, line_len - 1)
    # Above & Below
    str_above = lines[pos.line - 1][before_idx:after_idx + 1] if pos.line > 0 else ""
    str_below = lines[pos.line + 1][before_idx:after_idx + 1] if pos.line < (len(lines) - 1) else ""
    # Left or Right
    str_left = lines[pos.line][before_idx]
    str_right = lines[pos.line][after_idx]
    surrounding_chars = str_above + str_below + str_left + str_right
    return any((char not in non_symbol_chars) for char in surrounding_chars)


re_numbers = re.compile(r'\d+')
# Holds one tuple for each number, which represents the line the match is in,
# as well as the start-index and end-index of the number
number_coords: list[Coords] = []

counted_lines = enumerate(input_lines)
for i, line in counted_lines:
    number_coords.extend(Coords(i, match.start(), match.end()) for match in re_numbers.finditer(line))

# Part 1
valid_coords = filter(lambda nc: is_symbol_around(input_lines, nc), number_coords)
number_strings = map(lambda c: input_lines[c.line][c.start:c.end], valid_coords)
number_ints = map(int, number_strings)
print(f"Challenge 1: {sum(number_ints)}")

# Part 2
# TODO
