import itertools
from typing import NamedTuple

# Declare a lightweight type for the conversions
Conversion = NamedTuple("Conversion", range=range, delta=int)


def conversion_from_line(line: str) -> Conversion:
    """
    Take 3 space-separated numbers and create a Conversion object from them.
    According to the puzzle description, the meaning of the numbers is as follows:
    1. destination range start
    2. source range start
    3. range size
    """
    dest_start, source_start, range_size = [int(x) for x in line.strip().split()]
    return Conversion(range(source_start, source_start + range_size), delta=(dest_start - source_start))


def apply_conversions(conversions: list[list[Conversion]], num: int) -> int:
    for mappings in conversions:
        for mapping in mappings:
            # Check if the conversion applies to this number (= is within the range).
            # If it does, apply the delta and end this conversion category, as we were successful.
            if num in mapping.range:
                num += mapping.delta
                break
    return num


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]

    # Get the seed numbers from the first line, starting after "seeds:"
    seeds = [int(num) for num in input_lines[0][6:].strip().split()]
    # Store all conversions of one mapping in a list, then each of those lists in another list, so iterating is easy.
    conversions: list[list[Conversion]] = []
    # Truncate the header from the input so only the mapping remain.
    # Also filter the "... map:" headlines, as an empty line is sufficient as separator
    mapping_line_gen = (line for line in input_lines[3:] if "map:" not in line)

    # Use itertools.takewhile to iterate over input-lines until an empty line is found.
    # Using list(takewhile) will collect these lines (all mappings of one category) in a list and assign it to list_chunk.
    # When the condition is checked again, takewhile will continue where it stopped, as *the same generator object is used*.
    # The end-condition of takewhile will consume the empty line, so it will start with the line after that.
    # This approach eventually returns empty lists, when the generator is exhausted. As empty lists are falsy,
    # the while-loop will terminate, since list_chunk is assigned an empty list.
    while list_chunk := list(itertools.takewhile(lambda line: line.strip(), mapping_line_gen)):
        conversions.append([conversion_from_line(line) for line in list_chunk])

    # Part 1
    transformed_seeds = [apply_conversions(conversions, seed) for seed in seeds]
    print(f"Challenge 1: {min(transformed_seeds)}")

    # Part 2
    # Doing this like part 1 using exhaustive calculations is not sufficient, as there are billions of input values,
    # causing the script to run for an unknown amount of time. One could solve this by spending Cyprus's GDP on Cloud,
    # or being a little more clever and calculating only what is really necessary.
    # To determine the minimum result value, it is sufficient to look at the ranges, how they are converted by
    # the mappings and later at the lowest value available in the ranges.
    seed_ranges = [range(start, start + size) for start, size in zip(seeds[0::2], seeds[1::2])]
    for mappings in conversions:
        seed_ranges_gen = (split_range_by_conversions(r, mappings) for r in seed_ranges)
        # Flatten the list of lists to one list of ranges
        seed_ranges = sum(seed_ranges_gen, [])
        seed_ranges.sort(key=lambda r: r.start)
    lowest_result = min(r.start for r in seed_ranges if len(r) > 0)
    print(f"Challenge 2: {lowest_result}")


def split_range_by_conversions(r: range, conversions: list[Conversion]) -> list[range]:
    # Filter conversions which are irrelevant, as they're out of range.
    # This also guarantees that we can rely on ranges created from conversion to be within the original range's bounds.
    conversions = [c for c in conversions if not (c.range.stop < r.start or c.range.start > r.stop)]
    if len(conversions) == 0:
        return [r]
    conversions.sort(key=lambda c: c.range.start)
    first_range = range(r.start, conversions[0].range.start)
    last_range = range(conversions[-1].range.stop, r.stop)
    # Create ranges for each conversion, spanning their destination range after the conversion.
    conv_ranges = [range(max(c.range.start, r.start) + c.delta, min(c.range.stop, r.stop) + c.delta) for c in
                   conversions]
    # Between stop of one range and start of another are numbers which aren't modified either - these are relevant too
    inter_ranges = [range(c1.range.stop, c2.range.start) for c1, c2 in zip(conversions, conversions[1:])]
    return sorted([first_range, last_range] + conv_ranges + inter_ranges, key=lambda r: r.start)


if __name__ == '__main__':
    main()
