import itertools
import math

with open(f'{__file__.split(".")[0]}.txt', mode="r") as f:
    # Leading and trailing spaces matter in this challenge, so do not strip() lines here
    input_lines = [l.strip() for l in f.readlines()]


def line_to_ints(line: str) -> tuple[int, int]:
    x_str, y_str = line.split(",")
    return int(x_str), int(y_str)


def area(a: tuple[int, int], b: tuple[int, int]) -> int:
    return math.prod(abs(x - y) + 1 for x, y in zip(a, b))


def vsub(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return tuple((x - y for x, y in zip(a, b)))


def vadd(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return tuple(*(x + y for x, y in zip(a, b)))


if __name__ == "__main__":
    tiles = [line_to_ints(line) for line in input_lines]

    # Part 1
    tile_combinations = itertools.combinations(tiles, 2)
    biggest_tile_area = max(itertools.starmap(area, tile_combinations))
    print(f"Part 1: {biggest_tile_area}")

    # Part 2
    vectors = [vsub(v2, v1) for v1, v2 in itertools.pairwise(tiles + tiles[:1])]
