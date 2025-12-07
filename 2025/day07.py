import itertools as it
from collections import defaultdict

with open(f'{__file__.split(".")[0]}.txt', mode="r") as f:
    # Leading and trailing spaces matter in this challenge, so do not strip() lines here
    input_lines = [l.strip() for l in f.readlines()]


def split_beams(beam_idxs: set[int], splitter_idx: set[int]) -> tuple[set[int], int]:
    """ Takes indices of beams and splitters, returning all beam indices after splitting,"""
    splitter_results = [(s_idx - 1, s_idx + 1) for s_idx in splitter_idx if s_idx in beam_idxs]
    new_beams = set(it.chain(*splitter_results))
    # All beams that are in "beam_idx" but not in "splitter_idx", plus all beams in new_beams
    all_beams = beam_idxs - splitter_idx | new_beams
    return all_beams, len(splitter_results)


def find_splitters(s: str) -> set[int]:
    return {i for i, char in enumerate(s) if char == "^"}


if __name__ == "__main__":
    start_index = input_lines[0].index("S")
    splitter_lines = [line for line in input_lines[1:] if "^" in line]

    # Part 1
    iter_lines = iter(splitter_lines)
    beam_indices = {start_index}
    total_splits_performed = 0
    for line in iter_lines:
        beam_indices, splits = split_beams(beam_indices, find_splitters(line))
        total_splits_performed += splits
    print(f"Part 1: {total_splits_performed}")

    # Part 2
    iter_lines = iter(input_lines)
    # Start with a single timeline at the starting index
    timelines = defaultdict(int, {next(iter_lines).index("S"): 1})
    for line in iter_lines:
        # Keep track of the amount of new timelines based on the existing ones
        new_timelines = defaultdict(int)
        # Go through each splitter index in the line and advance the amount of timelines on that index
        # into the two surrounding indices, effectively splitting them in two - then delete the original entry.
        for splitter in find_splitters(line):
            new_timelines[splitter - 1] += timelines[splitter]
            new_timelines[splitter + 1] += timelines[splitter]
            del timelines[splitter]
        # Timelines on each index, resulting from a split must be added to the existing count of timelines.
        for idx, count in new_timelines.items():
            timelines[idx] += count
    print(f"Part 2: {sum(timelines.values())}")
