from functools import cache


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Part 1
    shifted_rocks = push_north(tuple(input_lines))
    weight = calculate_weight(shifted_rocks)
    print(f"Challenge 1: {weight}")

    # Part 2
    cycled_rocks = tuple(input_lines)
    for i in range(1000000000):
        cycled_rocks = do_cycle(cycled_rocks)
        if i % 10 ** 7 == 1:
            done_percentage = i / 1000000000
            print(f"Done with {done_percentage * 100:.0f}%")
    weight = calculate_weight(cycled_rocks)
    print(f"Challenge 2: {weight}")


@cache
def do_cycle(lines: tuple[str]) -> tuple[str]:
    lines = push_north(lines)
    lines = push_west(lines)
    lines = push_south(lines)
    lines = push_east(lines)
    return lines


def calculate_weight(lines: tuple[str]) -> int:
    rocks_per_line = [len(line.replace("#", "").replace(".", "")) for line in lines]
    row_weights = [weight * rocks for weight, rocks in zip(range(len(lines), 0, -1), rocks_per_line)]
    return sum(row_weights)


@cache
def push_north(lines: tuple[str]) -> tuple:
    # Transpose the lines, so colunns become rows
    lines = zip(*lines)
    sorted_lines = (sort_line(line) for line in lines)
    # Re-Transpose into original orientation
    return tuple("".join(column) for column in zip(*sorted_lines))


@cache
def push_south(lines: tuple[str]) -> tuple:
    # Transpose the lines, so colunns become rows
    lines = zip(*lines)
    sorted_lines = (sort_line(line, rocks_first=False) for line in lines)
    # Re-Transpose into original orientation
    return tuple("".join(column) for column in zip(*sorted_lines))


@cache
def push_west(lines: tuple[str]) -> tuple:
    sorted_lines = (sort_line(line) for line in lines)
    # Re-Transpose into original orientation
    return tuple(sorted_lines)


@cache
def push_east(lines: tuple[str]) -> tuple:
    sorted_lines = (sort_line(line, rocks_first=False) for line in lines)
    # Re-Transpose into original orientation
    return tuple(sorted_lines)


@cache
def sort_line(line: str | list[str] | tuple[str], rocks_first: bool = True) -> str:
    if isinstance(line, (list, tuple)):
        line = "".join(line)
    # Sorting the string in reverse-mode puts "O"-characters before "."-characters
    sorted_segments = ("".join(sorted(segment, reverse=rocks_first)) for segment in line.split("#"))
    return "#".join(sorted_segments)


if __name__ == '__main__':
    main()
