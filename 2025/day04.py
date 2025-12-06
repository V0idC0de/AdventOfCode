import itertools
from collections import Counter
import time
from typing import Iterable

with open(f'{__file__.split(".")[0]}.txt', mode="r") as f:
    input_lines = [l.strip() for l in f.readlines()]


def neighbor_idxs(idx: int, row_len: int, total_len: int) -> tuple[int, ...]:
    """ Find all neighboring indices within bounds (total_len is an exclusive index)."""
    left = (idx - 1 - row_len), (idx - 1), (idx - 1 + row_len)
    right = (idx + 1 - row_len), (idx + 1), (idx + 1 + row_len)
    surrounding = itertools.chain(
        [idx - row_len, idx + row_len],  # top and bottom
        left if idx % row_len != 0 else (),
        right if (idx + 1) % row_len != 0 else ()
    )
    filter_out_of_bounds = filter(lambda x: 0 <= x < total_len, surrounding)
    return tuple(filter_out_of_bounds)


def available_rolls(inventory: Iterable[int], row_len: int) -> list[int]:
    paper_indices = list(i for i, is_paper in enumerate(inventory) if is_paper)
    paper_neighbors = (neighbor_idxs(idx, row_len, len(inventory)) for idx in paper_indices)
    roll_neighbor_idxs = (filter(lambda idx: inventory[idx], itertools.chain.from_iterable(paper_neighbors)))
    # Count how many times each index appears as a neighbor of a paper roll
    counted = Counter(roll_neighbor_idxs)
    # Iterate over paper_indices, since rolls without any neighbors do not appear in the Counter at all, but are valid
    available_rolls = [idx for idx in paper_indices if counted.get(idx, 0) < 4]
    return available_rolls


if __name__ == "__main__":
    start_time = time.perf_counter_ns()

    row_len = len(input_lines[0])

    # Part 1
    inventory = [s == "@" for s in "".join(input_lines)]
    print(f"Part 1: {len(available_rolls(inventory, row_len))}")

    # Part 2
    inventory = [s == "@" for s in "".join(input_lines)]
    removed_rolls = 0
    while rolls := available_rolls(inventory, row_len):
        for idx in rolls:
            inventory[idx] = False
        removed_rolls += len(rolls)
    print(f"Part 2: {removed_rolls}")

    end_time = time.perf_counter_ns()
    print(f"Execution time: {(end_time - start_time) / 1_000_000} ms")
