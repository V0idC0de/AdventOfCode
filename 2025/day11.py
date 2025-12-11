import math
from collections.abc import Mapping
from functools import cache

with open(f'{__file__.split(".")[0]}.txt', mode="r") as f:
    # Leading and trailing spaces matter in this challenge, so do not strip() lines here
    input_lines = [l.strip() for l in f.readlines()]


def line_to_tuple(line: str) -> tuple[str, tuple[str, ...]]:
    parts = line.split()
    return parts[0].strip(":"), tuple(parts[1:])


def find_possible_paths(connections: dict[str, tuple[str, ...]], start: str, end: str) -> int:
    @cache
    def possible_paths(start_mode: str) -> int:
        if start_mode == end:
            return 1
        return sum(possible_paths(conn) for conn in connections.get(start_mode, []))

    return possible_paths(start)


if __name__ == '__main__':
    line_tuples = (line_to_tuple(line) for line in input_lines)
    available_connections = dict(line_tuples)

    # Part 1
    amount_paths = find_possible_paths(available_connections, "you", "out")
    print(f"Part 1: {amount_paths}")

    # Part 2
    # Find all paths that lead from the start to either fft or dac
    start_to_fft = find_possible_paths(available_connections, "svr", "fft")
    start_to_dac = find_possible_paths(available_connections, "svr", "dac")
    # Find all paths between fft and dac - pathing is not symmetrical, so find both directions
    fft_to_dac = find_possible_paths(available_connections, "fft", "dac")
    dac_to_fft = find_possible_paths(available_connections, "dac", "fft")
    # Find all paths from either fft or dac to the end
    fft_to_out = find_possible_paths(available_connections, "fft", "out")
    dac_to_out = find_possible_paths(available_connections, "dac", "out")

    total_paths = (start_to_fft * fft_to_dac * dac_to_out) + (start_to_dac * dac_to_fft * fft_to_out)
    print(f"Part 2: {total_paths}")
