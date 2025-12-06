import itertools
import time
from collections.abc import Generator
from typing import Iterable

with open(f'{__file__.split(".")[0]}.txt', mode="r") as f:
    input_lines = [l.strip() for l in f.readlines()]


def line_to_range(line: str) -> range:
    start, end = map(int, line.split("-"))
    return range(start, end + 1)


def compact_ranges(ranges: Iterable[range]) -> Generator[range]:
    iter_ranges_sorted = iter(sorted(ranges, key=lambda r: r.start))
    # Bootstrap with the value of our first range
    first_range = next(iter_ranges_sorted)
    current_start, current_stop = first_range.start, first_range.stop
    # Continue the Iterator by using it with this for-loop, as it will start from the second element
    for r in iter_ranges_sorted:
        if r.start <= current_stop:
            # Ranges are seamlessly connected or overlap - just move the current_stop number
            current_stop = max(current_stop, r.stop)
        else:
            # Ranges have a gap of at least one ID -
            yield range(current_start, current_stop)
            current_start, current_stop = r.start, r.stop
    # Yield everything left in the loop
    yield range(current_start, current_stop)


if __name__ == "__main__":
    start_time = time.perf_counter_ns()

    iter_lines = iter(input_lines)
    # Advance iterator and take lines until the blank line
    fresh_lines = itertools.takewhile(lambda s: s.strip(), iter_lines)
    fresh_ranges = map(line_to_range, fresh_lines)
    # Summarize Ranges by combining seamlessly connected or overlapping ranges
    summarized_ranges = list(compact_ranges(fresh_ranges))

    # Continue Iterator `iter_lines`, which is currently at the blank line separating the fresh ranges from ingredients.
    # All remaining lines are ingredient IDs.
    ingredients = list(map(int, iter_lines))

    # Part 1
    # Count by summing up 1 for ingredient IDs, which are present in any of the ranges
    fresh_ings = sum(1 for ing_id in ingredients if any(ing_id in fresh_ids for fresh_ids in summarized_ranges))
    print(f"Part 1: {fresh_ings}")

    # Part 2
    print(f"Part 2: {sum(map(len, summarized_ranges))}")

    end_time = time.perf_counter_ns()
    print(f"Execution time: {(end_time - start_time) / 1_000_000} ms")
