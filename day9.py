from typing import Tuple, List, Set

# ### Uses the day9-test.txt input to replay an example from the explanation
# with open(f'{__file__.split(".")[0]}-test.txt') as f:
with open(f'{__file__.split(".")[0]}.txt') as f:
    moves = [l.strip("\n") for l in f.readlines()]

move_distances = {
    "U": (0, -1),
    "D": (0, 1),
    "R": (1, 0),
    "L": (-1, 0)
}


def delta_to_move_tuple(x_delta: int, y_delta) -> tuple[int, int]:
    # Creates a move tuple the following knot will take, based on the positional difference to the leading knot.
    # If the delta between two rope knots is 2 or more fields away in either X or Y direction, a move is triggered.
    # The knot then moves 1 field in X and/or Y direction, if their respective delta is anything other than 0.
    # Move distance is always 1 or -1, as a rope knot cannot move away 2 fields in one dimension using a single move.
    if abs(x_delta) >= 2 or abs(y_delta) >= 2:
        return (
            x_delta // abs(x_delta) if x_delta != 0 else 0,
            y_delta // abs(y_delta) if y_delta != 0 else 0,
        )
    # If none of the absolute deltas is 2 or more, no tail-move happens at all
    return 0, 0


def visualize_field(dot_list: List[Tuple[int, int]]) -> None:
    field = []
    field_perimeter = 26
    visual_offset = 10
    for _ in range(field_perimeter):
        field.append("." * field_perimeter)
    for i, dot in reversed(list(enumerate(dot_list))):
        x, y = dot
        x, y = x + visual_offset, y + visual_offset
        if x < 0 or y < 0:
            continue
        field[y] = f"{field[y][:x]}{i}{field[y][x + 1:]}"
    print("\n" * 5)
    for line in field:
        print(" ".join(line))


def calculate_tail_positions(rope_length: int, move_list: List[str]) -> Set[Tuple[int, int]]:
    visited_fields = set()
    dot_list: List[Tuple[int, int]] = [(0, 0) for _ in range(rope_length)]

    for turn_no, move in enumerate(move_list):
        # Split move and iterations
        direction, iterations = move.split()
        direction_tuple = move_distances[direction]
        for _ in range(int(iterations)):
            # Handle head-move
            dot_list[0] = dot_list[0][0] + direction_tuple[0], dot_list[0][1] + direction_tuple[1]
            # visualize_field(dot_list)
            # Let the tail catch up
            for i in range(1, len(dot_list)):
                x_move, y_move = delta_to_move_tuple(dot_list[i - 1][0] - dot_list[i][0],
                                                     dot_list[i - 1][1] - dot_list[i][1])
                dot_list[i] = dot_list[i][0] + x_move, dot_list[i][1] + y_move
                # visualize_field(dot_list)
            # Add the tail position to discovered fields
            visited_fields.add(dot_list[-1])
    return visited_fields


print(f"Part 1: Rope Tail for length 2 visited {len(calculate_tail_positions(2, moves))} field(s)!")
print(f"Part 2: Rope Tail for length 10 visited {len(calculate_tail_positions(10, moves))} field(s)!")
