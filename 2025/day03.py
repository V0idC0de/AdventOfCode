import time

with open(f'{__file__.split(".")[0]}.txt', mode="r") as f:
    input_lines = [l.strip() for l in f.readlines()]


def find_max(row: list[int]) -> tuple[int, int]:
    """
    For a list of integers `row`, find the highest integer and return (idx, value),
    where `idx` is the index of the highest integer in the list and `value` is the integer itself.
    """
    highest_int = max(row)
    return row.index(highest_int), highest_int


def highest_joltage(row: list[int], enabled_batteries: int) -> int:
    """
    For a list of integers `row`, use the highest `enabled_batteries` integers, so their concatenation is maximized.
    Return the resulting concatenated integer.
    """
    if enabled_batteries == 0:
        return 0
    # Leave at enough batteries, so `enabled_batteries` can still be selected.
    max_idx, max_value = find_max(row[:len(row) - enabled_batteries + 1])
    # If 3 batteries should be enabled, the first battery contributes in the magnitude of 10^2,
    # so `(enabled_batteries - 1)` is the exponent for the current battery's joltage.
    joltage = max_value * 10 ** (enabled_batteries - 1)
    # Return the sum of the current joltage, plus the joltage of the remaining batteries after this one.
    return joltage + highest_joltage(row[max_idx + 1:], enabled_batteries - 1)


if __name__ == "__main__":
    start_time = time.perf_counter_ns()

    batteries = [[int(j) for j in row] for row in input_lines]
    # Part 1
    joltages = [highest_joltage(row, enabled_batteries=2) for row in batteries]
    print(f"Part 1: {sum(joltages)}")

    # Part 2
    big_joltages = [highest_joltage(row, enabled_batteries=12) for row in batteries]
    print(f"Part 2: {sum(big_joltages)}")

    end_time = time.perf_counter_ns()
    print(f"Execution time: {(end_time - start_time) / 1_000_000} ms")
