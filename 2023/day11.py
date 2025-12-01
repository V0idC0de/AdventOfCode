import itertools


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]

    empty_rows = [i for i, line in enumerate(input_lines) if set(line) == {"."}]
    empty_cols = [i for i, col in enumerate(zip(*input_lines)) if set(col) == {"."}]
    coords = itertools.product(range(len(input_lines)), range(len(input_lines[0])))
    galaxies = {(row, col) for row, col in coords if input_lines[row][col] == "#"}
    galaxy_pairs = {(g1, g2) for g1, g2 in itertools.combinations(galaxies, 2)}

    # Part 1
    distances = [galaxy_distance(g1, g2, empty_rows, empty_cols, 1) for g1, g2 in galaxy_pairs]
    print(f"Challenge 1: {sum(distances)}")

    # Part 2
    distances = [galaxy_distance(g1, g2, empty_rows, empty_cols, 10 ** 6) for g1, g2 in galaxy_pairs]
    print(f"Challenge 1: {sum(distances)}")


def galaxy_distance(g1: tuple[int, int],
                    g2: tuple[int, int],
                    empty_rows: list[int],
                    empty_cols: list[int],
                    expansion_factor: int) -> int:
    """
    Colculates the distance between `g1` and `g2`, considering each crossed row or column present in `empty_rows` or
    `empty_cols` respectively, as `expansion_factor`-times as big. The puzzle asks for twice as big (factor = 2) and
    one million times as big (factor = 1.000.000).

    :return: Calculates distance between `g1` and `g2`
    """
    # noinspection PyTupleAssignmentBalance
    g1_row, g1_col, g2_row, g2_col = *g1, *g2
    rows = set(range(min(g1_row, g2_row), max(g1_row, g2_row)))
    cols = set(range(min(g1_col, g2_col), max(g1_col, g2_col)))
    row_distance = len(rows) + len(rows.intersection(empty_rows)) * (expansion_factor - 1)
    col_distance = len(cols) + len(cols.intersection(empty_cols)) * (expansion_factor - 1)
    return row_distance + col_distance


if __name__ == '__main__':
    main()
