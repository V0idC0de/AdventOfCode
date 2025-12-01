import itertools

directions = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1)
}


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip().split() for line in f.readlines()]

    # Part 1
    instructions: list[tuple[str, int]] = [(direction, int(x)) for direction, x, _ in input_lines]
    borders = get_border_fields(instructions)
    filled_space = fill_space(borders)
    total_holes = borders.union(filled_space)
    print(f"Challenge 1: {len(total_holes)}")

    # Part 2
    # This won't finish anytime soon. Time-complexity is too high and the input too large.
    # For the better approach, see README.md - I'm honestly too bored of the part2-time-complexity tasks to do this rn.
    direction_map = {"0": "R", "1": "D", "2": "L", "3": "U"}
    instructions: list[tuple[str, int]] = [(direction_map[color[-2]], int(color[2:-2], 16)) for _, _, color in
                                           input_lines]
    borders = get_border_fields(instructions)
    filled_space = fill_space(borders)
    total_holes = borders.union(filled_space)
    print(f"Challenge 2: {len(total_holes)}")


def fill_space(borders: set[tuple[int, int]]) -> set[tuple[int, int]]:
    root_node = next(iter(borders), None)
    if root_node is None:
        return set()
    min_x, max_x = min(x for x, _ in borders), max(x for x, _ in borders)
    min_y, max_y = min(y for _, y in borders), max(y for _, y in borders)

    # All combinations of directions, unless they cancel each other out -> basically all diagonal directions
    diagonals = filter(lambda t: t != (0, 0),
                       map(lambda tuples: tuple(a + b for a, b in zip(*tuples)),
                           itertools.combinations(directions.values(), 2)))
    # If a node is part of the border, at least one of the diagonal nodes is not a border and part of the inner area
    start_nodes = [(root_node[0] + delta_x, root_node[1] + delta_y) for delta_x, delta_y in diagonals]
    for s_node in start_nodes:
        suspect_fields = {s_node}
        filled_area = set()
        while len(suspect_fields):
            x, y = field = suspect_fields.pop()
            if field in borders:
                continue
            elif not (min_x <= x <= max_x) or not (min_y <= y <= max_y):
                # Field is not part of the borders, but is at the edge of the grid, hence not surrounded by any border.
                # This cannot be the area we're looking for, so continue with the next, by discarding this s_node.
                filled_area = set()
                break
            filled_area.add(field)
            adjacent_fields = [(x + delta_x, y + delta_y) for delta_x, delta_y in directions.values()]
            for field in adjacent_fields:
                if field not in borders and field not in filled_area:
                    suspect_fields.add(field)
        # If suspect_fields could be exhausted without running into an edge, the area is enclosed by borders
        if len(filled_area) > 0:
            return filled_area
    return set()


def get_border_fields(instructions: list[tuple[str, int]]) -> set[tuple[int, int]]:
    current_x, current_y = 0, 0
    known_holes: set[tuple[int, int]] = {(current_x, current_y)}
    for direction, steps, *_ in instructions:
        delta_x, delta_y = directions[direction]
        # Add all steps in between to the known_holes
        for i in range(1, steps + 1):
            known_holes.add((current_x + delta_x * i, current_y + delta_y * i))
        # Update the current position to the end of the dig-run.
        current_x, current_y = current_x + delta_x * steps, current_y + delta_y * steps
    return known_holes


if __name__ == '__main__':
    main()
