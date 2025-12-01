import itertools
from functools import cache


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = list(f.readline().strip().split(","))

    # Part 1
    hash_per_line = [hash_line(line) for line in input_lines]
    print(f"Challenge 1: {sum(hash_per_line)}")

    # Part 2
    # Dicts are ordered by default since Python 3.7, so using collections.OrderedDict is not necessary
    boxes = [dict() for _ in range(256)]
    for line in input_lines:
        # For some reason, Type Checker complains that str.isalpha supposedly has wrong typing for takewhile().
        # noinspection PyTypeChecker
        label = "".join(itertools.takewhile(str.isalpha, line))
        box, is_removal, length = hash_line(label), ("-" in line), line[-1]
        if is_removal:
            boxes[box].pop(label, None)
        else:
            boxes[box][label] = int(length)

    powers = [i * focusing_power(box) for i, box in enumerate(boxes, start=1)]
    print(f"Challenge 2: {sum(powers)}")


def focusing_power(box: dict[str, int]) -> int:
    return sum(i * length for i, length in enumerate(box.values(), start=1))


@cache
def hash_line(line: str) -> int:
    hash_val = 0
    for char in line:
        hash_val = hash_char(char, hash_val)
    return hash_val


@cache
def hash_char(char: str, init_value: int) -> int:
    return ((init_value + ord(char)) * 17) % 256


if __name__ == '__main__':
    main()
