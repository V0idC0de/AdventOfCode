import itertools
from collections.abc import Generator
from typing import Literal

Direction = Literal["N", "S", "E", "W"]
direction_map: dict[Direction, tuple[int, int]] = {
    "N": (-1, 0),
    "S": (1, 0),
    "E": (0, 1),
    "W": (0, -1)
}
pipes: dict[str, tuple[Direction, Direction | None]] = {
    # Directions are alphabetically ordered, so that searching for the replacement of "S",
    # based on the locations it is pointing to, becomes easier.
    "|": ("N", "S"),
    "-": ("E", "W"),
    "L": ("E", "N"),
    "J": ("N", "W"),
    "7": ("S", "W"),
    "F": ("E", "S"),
}


def redirect(pipe: str, enter_direction: Direction) -> Direction | None:
    """
    Calculate the new direction after visiting `pipe` from `enter_direction`.
    If `pipe` cannot be entered from `enter_direction` or `pipe` is not walkable at all or unknown,
    `None` is returned to indicate a dead end.

    :param pipe: Letter representing the pipe on the field to be entered.
    :param enter_direction: `Direction` string which represents the direction from which `pipe` is entered.
    :return: New `Direction` in which `pipe` will be exited through. `None`, if `pipe` cannot be entered from
        `enter_direction` or is not a known pipe tile at all (= dead end).
    """
    # Enter direction is inverted, as entering in southern direction uses the pipes northern entrance.
    invert_map = {"S": "N", "N": "S", "E": "W", "W": "E"}
    enter_direction = invert_map[enter_direction]
    if enter_direction not in pipes.get(pipe, tuple()):
        return None
    return next(direction for direction in pipes[pipe] if direction != enter_direction)


def pipe_steps(pipe_map: list[str],
               start_pos: tuple[int, int],
               direction: Direction) -> Generator[tuple[int, int]]:
    """
    Generates the locations that are visited by following the pipes starting at `start_pos`.
    Generator will terminate on dead-ends.
    Will NOT return the starting position as first position, but start with the first new tile.

    :param pipe_map: `list` of `str` representing the individual pipes.
    :param start_pos: Position to start at in format `(row, column)`, effectively index in `pipe_map`
    :param direction: String representing the direction in which to move initially.
    :return: `tuple[int, int]` representing the position like `start_pos`.
    """
    while True:
        start_pos = tuple(x + y for x, y in zip(start_pos, direction_map[direction]))
        row, col = start_pos
        if not (0 <= row < len(pipe_map) and 0 <= col <= len(pipe_map[row])):
            # If any of the two indices run out-of-bounds on the pipe-map, no more steps are possible
            break
        pipe_char = pipe_map[row][col]
        direction = redirect(pipe_char, direction)
        if direction is None:
            break
        yield start_pos


def count_tile_in_loop(pipe_map: list[str], loop_tiles: list[tuple[int, int]]) -> int:
    tiles_in_loop = 0
    for row, line in enumerate(pipe_map):
        in_loop = False
        # Remember the last corner pipe
        last_corner = ""
        for col, char in enumerate(line):
            if (row, col) in loop_tiles:
                if char == "-":
                    pass
                elif char in ["-", "|"]:
                    in_loop = not in_loop
                # If corners are encountered, it is important to see, if the ending-corner's direction (up/down) is
                # the same as the starting-corner, to determine whether we're in the loop or out of the loop.
                # For reference, compare the first example of part 2 line 2, 3 and 6.
                # If the direction is the same, we stay in the same `in_loop` state as before, otherwise it's changed.
                elif char in ["L", "F"]:
                    last_corner = char
                elif char == "J":
                    in_loop = in_loop if last_corner == "L" else not in_loop
                elif char == "7":
                    in_loop = in_loop if last_corner == "F" else not in_loop
            elif in_loop:
                tiles_in_loop += 1
    return tiles_in_loop


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Search through each line for S and return index of the line itself and index of "S" in that line.
    # As per puzzle description, there is EXACTLY ONE "S" tile.
    start_pos = next((row, line.index("S")) for row, line in enumerate(input_lines) if "S" in line)
    # Puzzle states, that the "S" tile is connected to EXACTLY TWO pipes, so all others will be dead-ends.
    # We filter the possible directions by checking their next step, using the pipe-step-generator function.
    # If the direction hasn't a next step, it's a dead-end. Exactly two directions are valid, as per description.
    directions: list[Direction] = list(filter(lambda d: next(pipe_steps(input_lines, start_pos, d), None),
                                              direction_map.keys()))

    # Part 1
    walkers = zip(*(pipe_steps(input_lines, start_pos, d) for d in directions))
    walk_until_meet = itertools.takewhile(lambda positions: len(set(positions)) > 1, walkers)
    # As the last step towards the identical location is not generated by takewhile(),
    # as it already violates the condition, we need to add one step.
    steps_until_meet = sum(1 for step in walk_until_meet) + 1
    print(f"Challenge 1: {steps_until_meet}")

    # Part 2
    # noinspection PyTypeChecker
    s_replacement = {v: k for k, v in pipes.items()}.get(tuple(sorted(directions)))
    input_lines[start_pos[0]] = input_lines[start_pos[0]].replace("S", s_replacement)
    steps_along_loop = itertools.takewhile(lambda pos: pos != start_pos,
                                           pipe_steps(input_lines, start_pos, directions[0]))
    loop_tiles = [start_pos] + list(steps_along_loop)
    amount_tiles_in_loop = count_tile_in_loop(input_lines, loop_tiles)
    print(f"Challenge 2: {amount_tiles_in_loop}")


if __name__ == '__main__':
    main()
