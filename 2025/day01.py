from typing import Iterable

with open(f'{__file__.split(".")[0]}.txt') as f:
    input_lines = [l.strip() for l in f.readlines()]


def input_to_direction(line: str) -> int:
    """ Return a tuple of direction letter and the amount of steps to take (direction already considered as sign) """
    direction = line[0]
    steps = int(line[1:].strip())
    return -steps if direction == "L" else steps


def dial_wheel(moves: Iterable[int], dial_pos=50, max_number=99) -> Iterable[tuple[int, int]]:
    """
    Generator returning the current position on the dial wheel and amount of times "0" was touched after each dial.

    :param moves: Iterable of integers with the steps to take (positive = clockwise, negative = counter-clockwise)
    :param dial_pos: Starting position on the dial wheel
    :param max_number: Maximum number on the dial wheel (0 to max_number, inclusive)

    :return: Iterable of tuples containing the current position on the dial wheel and amount of wraparounds done
    """
    modulus = max_number + 1
    for steps in moves:
        # Calculate amount of wraparounds done
        result = dial_pos + steps
        wraps = abs(result) // modulus
        # Add a wrap if the dial_pos "underflow" past 0, unless it was already 0
        if result <= 0 and dial_pos != 0:
            wraps += 1

        # Update dial position
        dial_pos = (dial_pos + steps) % modulus
        yield dial_pos, wraps


if __name__ == "__main__":
    dial_inputs = list(map(input_to_direction, input_lines))

    # Part 1
    # Go through the moves and store the position, if it is 0.
    # Then count the length of that list.
    dial_positions = [x for x, _ in dial_wheel(dial_inputs) if x == 0]
    print(f"Part 1: {len(dial_positions)}")

    # Part 2
    dial_wraps = [wraps for _, wraps in dial_wheel(dial_inputs)]
    print(f"Part 2: {sum(dial_wraps)}")
