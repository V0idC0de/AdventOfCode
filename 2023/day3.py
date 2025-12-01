import itertools

with open(f'{__file__.split(".")[0]}.txt') as f:
    input_lines = [l.strip() for l in f.readlines()]

import re
from collections import namedtuple

Coords = namedtuple("Coords", "line start end value")


def surrounding_symbols(lines: list[str | list], pos: Coords, coords_only: bool = False) -> set:
    """
    Determines whether any symbol not listed in `non_symbol_chars` is in adjacent coordinates of `pos`.
    Diagonal is considered adjacent.

    :param lines: Lines of text, in which `pos` is a location
    :param pos: Position within the char-grid `lines` to check. Declares line number and an index-range in the line.
    :param coords_only: Only return `Coords` objects in the return set. Relevant for part 2 of the challenge.
    :return: Set of symbols not listed in `non_symbol_chars` is adjacent to `pos` in `lines`.
    """
    line_len = len(lines[0])
    non_symbol_chars = {".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
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
    # Gather all surrounding objects in one set to eliminate duplicates.
    # This is especially relevant for part 2 of the challange.
    surrounding_chars = {*str_above, *str_below, str_left, str_right}
    if coords_only:
        surrounding_chars = {obj for obj in surrounding_chars if isinstance(obj, Coords)}
    return surrounding_chars.difference(non_symbol_chars)


re_numbers = re.compile(r'\d+')
# Holds one tuple for each number, which represents the line the match is in,
# as well as the start-index and end-index of the number
number_coords: list[Coords] = []

for i, line in enumerate(input_lines):
    number_coords.extend(Coords(i,
                                match.start(),
                                match.end(),
                                int(input_lines[i][match.start():match.end()])) for match in re_numbers.finditer(line))

# Part 1
# Get all those coordinates, which have at least one symbol around them (= function return value is not {})
valid_coords = filter(lambda nc: surrounding_symbols(input_lines, nc), number_coords)
print(f"Challenge 1: {sum(c.value for c in valid_coords)}")

# Part 2
# Make the grid a list of lists with one character or NamedTuple each, so it's easier to mutate
number_grid: list[list[str | Coords]] = [list(line) for line in input_lines]
# Place the Coords object in place of each digit it consists of, so we can instantly find the full number if we come
# across a digit. This also allows us to easily check, whether two digits belong to the same number (= same object).
for c in number_coords:
    for idx in range(c.start, c.end):
        number_grid[c.line][idx] = c

# Go through all coordinates in the grid and find all "*" fields
height, width = len(number_grid), len(number_grid[0])
coord_iter = itertools.product(range(height), range(width))
star_coords = [Coords(i, j, j + 1, 0) for i, j in coord_iter if number_grid[i][j] == "*"]
# Using the same function, we find all objects in coordinates around the asterisk character, specifically the numbers.
# As it returns a set, so each number (or rather tuple representing a number) only once, we can easily check if there
# are exactly two numbers around that asterisk.
gear_factor_coords = [list(surrounding_symbols(number_grid, c)) for c in star_coords]
# Filter the chunks of numbers around the asterisk characters for the ones with exactly two factors.
gear_products = [coords[0].value * coords[1].value for coords in gear_factor_coords if len(coords) == 2]
print(f"Challenge 2: {sum(gear_products)}")
