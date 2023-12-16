from functools import cache
from queue import Queue
from typing import Literal

Direction = Literal["<", ">", "^", "v"]
Beam = tuple[tuple[int, int], Direction]


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Part 1
    # Length of visited tiles minus 1 for the out-of-bounds starting tile
    energy = len(simulate_beams(input_lines, ((0, -1), ">")))
    print(f"Challenge 1: {energy}")

    # Part 2
    start_locations: list[Beam] = [
        *[((-1, col), "v") for col in range(len(input_lines[0]))],
        *[((row, len(input_lines[0])), "<") for row in range(len(input_lines))],
        *[((len(input_lines), col), "^") for col in range(len(input_lines[0]))],
        *[((row, -1), ">") for row in range(len(input_lines))],
    ]
    highest_energy = max(len(simulate_beams(input_lines, loc)) for loc in start_locations)
    print(f"Challenge 2: {highest_energy}")


def simulate_beams(grid: list[str], start_location: Beam) -> set[tuple[int, int]]:
    """
    Takes the mirror grid and a starting location (it should be out-of-bounds by 1 and head into the direction of the
    grid. This additional tile will be subtracted from the resulting `set` of visited tiles
    :return: `set` containing a `tuple[int, int]` for each visited field, not including the `start_location` one.
    """
    known_beam_steps: set[Beam] = set()
    beams: Queue[Beam] = Queue()
    beams.put(start_location)

    while not beams.empty():
        beam = beams.get()
        for next_beam in next_beams(tuple(grid), beam):
            if next_beam not in known_beam_steps:
                beams.put(next_beam)
                known_beam_steps.add(next_beam)

    return {tile for tile, _ in known_beam_steps}


@cache
def next_beams(grid: tuple[str, ...], beam: Beam) -> list[Beam]:
    dir_to_delta: dict[Direction, tuple[int, int]] = {
        "<": (0, -1),
        ">": (0, 1),
        "^": (-1, 0),
        "v": (1, 0)
    }
    location, direction = beam
    delta = dir_to_delta[direction]
    new_loc_row, new_loc_col = location[0] + delta[0], location[1] + delta[1]
    # Check if the beam goes out-of-bounds
    if not (0 <= new_loc_row < len(grid)) or not (0 <= new_loc_col < len(grid[0])):
        return []

    if grid[new_loc_row][new_loc_col] == "|" and direction in ["<", ">"]:
        return [((new_loc_row, new_loc_col), "^"), ((new_loc_row, new_loc_col), "v")]
    if grid[new_loc_row][new_loc_col] == "-" and direction in ["^", "v"]:
        return [((new_loc_row, new_loc_col), "<"), ((new_loc_row, new_loc_col), ">")]
    if grid[new_loc_row][new_loc_col] == "/":
        mirror_map = {"^": ">", ">": "^", "v": "<", "<": "v"}
        return [((new_loc_row, new_loc_col), mirror_map[direction])]
    if grid[new_loc_row][new_loc_col] == "\\":
        mirror_map = {"^": "<", ">": "v", "v": ">", "<": "^"}
        return [((new_loc_row, new_loc_col), mirror_map[direction])]
    return [((new_loc_row, new_loc_col), direction)]


if __name__ == '__main__':
    main()
