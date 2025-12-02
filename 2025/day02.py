import itertools
import math
import time
from typing import Iterable

import numba

with open(f'{__file__.split(".")[0]}.txt', mode="r") as f:
    input_lines = [l.strip() for l in f.readlines()]

ranges = [r.split("-") for r in input_lines[0].split(",")]
ranges = [(int(x), int(y)) for x, y in ranges]


@numba.njit
def id_repeats(n: int) -> bool:
    n_len = math.floor(math.log10(n)) + 1
    # i = length of repeating number
    for i in range(1, (n_len // 2 + 1), 1):
        # If i doesn't divide n_len without remainder, i cannot be repeated cleanly in n_len
        if n_len % i != 0:
            continue
        # Construct a multiplier to repeat a number of length i
        # like 80, 8080, 808080 by having a multiplier of 80 * 1 or 80 * 101 or 80 * 10101.
        # This works by summing up the 10^e where e is each number of 0 up to the magnitude of n,
        # but minus n_len, to account for the magnitude of n.
        multiplicator = 0
        for m in range(0, n_len - i + 1, i):
            multiplicator += 10 ** m

        # Grab the highest i digits of n. This could be done via string-slicing,
        # but the aim of this solution is to work mostly without string-manipulation.
        repeated_number = n // 10 ** (n_len - i)

        # Check whether multiplying `repeated_number` with `multiplicator` (which causes the number to repeat)
        # results in n. Return True, if a match is found.
        if repeated_number * multiplicator == n:
            return True
    return False


@numba.njit
def id_repeats_twice(n: int) -> bool:
    n_len = math.floor(math.log10(n)) + 1
    # If length is odd, a number cannot cleanly repeat twice, implying it is valid.
    if n_len % 2 == 1:
        return False
    # Integer-division doesn't drop a float-portion, since n_len is always even at this point.
    multiplier = (10 ** (n_len // 2)) + 1
    # Grab the first half of n's digits. This could be done via string-slicing,
    # but the aim of this solution is to work mostly without string-manipulation.
    repeated_number = n // 10 ** (n_len // 2)
    # Calculate the number that results from multiplying the repetition-multiplier and half the digits of n.
    # If it matches, the number is repeating, thus returning True, otherwise False.
    return repeated_number * multiplier == n


def find_invalid_ids(ranges_list: list[tuple[int, int]], only_twice: bool = False) -> Iterable[int]:
    """
    Takes a list of tuples, each having a start and end number (inclusive) and checks each number within them.
    A number `n` of these ranges is returned, if it consists of a number, cleanly repeated throughout `n`.
    """
    is_repeating = id_repeats_twice if only_twice else id_repeats
    ranges = (range(x, y + 1) for x, y in ranges_list)
    for n in itertools.chain(*ranges):
        if is_repeating(n):
            yield n


def check_range(start: int, end: int, only_twice: bool = False) -> tuple[int, ...]:
    """
    Takes a start and end number (inclusive) and checks each number within them.
    A number `n` of this range is returned, if it consists of a number, cleanly repeated throughout `n`.
    """
    is_repeating = id_repeats_twice if only_twice else id_repeats
    return tuple(n for n in range(start, end + 1) if is_repeating(n))


if __name__ == "__main__":
    start_time = time.time_ns()
    # Part 1
    invalid_ids = list(find_invalid_ids(ranges, only_twice=True))
    print(f"Part 1: {sum(invalid_ids)}")

    # Part 2
    repeating_ids = find_invalid_ids(ranges, only_twice=False)
    print(f"Part 2: {sum(repeating_ids)}")
    end_time = time.time_ns()
    print(f"Execution time: {(end_time - start_time) / 1_000_000} ms")
