"""
This day contains quite a lot of unused ideas and experiments, since it took me several hours of fiddling and a few
hits from Reddit to complete. I left the function in here for the lulz of what I tried and what failed (everything
including brute-force or trial-and-error-recursion failed).
"""

import itertools
import re
from collections.abc import Iterable
from functools import lru_cache
from typing import Generator


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]
    lines = [line.split() for line in input_lines]

    # Part 1
    possibilities_per_line = ((possible_patterns(line), pattern_to_regex(pattern)) for line, pattern in lines)
    options_per_line = (count_valid_patterns(s, regex) for s, regex in possibilities_per_line)
    # options_per_line = (guess_next_char(s, pattern) for s, pattern in lines)
    print(f"Challenge 1: {sum((options for options in options_per_line))}")

    # Part 2
    lines = [("?".join([line] * 5), ",".join([pattern] * 5)) for line, pattern in lines]
    lines = [(line, tuple(int(i) for i in patterns.split(","))) for line, patterns in lines]
    print(f"Challenge 2: {sum(count_automaton(line, patterns) for line, patterns in lines)}")


def count_automaton(line: str, patterns: tuple[int, ...]) -> int:
    """
    Heavily inspired by https://github.com/clrfl/AdventOfCode2023/blob/master/12/part2.py.
    Tried for many hours to implement a more optimized version of part 1, which ended up working, but still took
    (predicted) an hour or something to complete.
    Manageable, but obviously not a nice choice - however, I couldn't think of more optimizations.
    The NFA (Non-Deterministic Finite Automaton) solution was super smart, using a completely different approach and
    I was quite impressed and frustrated, since I didn't understand why it worked, at first.
    After thinking about it for a while, I fiddled with my own NFA implementation and ended up with a very similar
    solution. I spared the leading "." at `states` however - still don't understand what it is used for.
    """
    states = ".".join("#" * pattern for pattern in patterns) + "."
    progressions = {0: 1}
    next_progressions = {}
    for char in line:
        for progress in progressions.keys():
            if char == "?":
                if progress + 1 < len(states):
                    next_progressions[progress + 1] = next_progressions.get(progress + 1, 0) + progressions[progress]
                if states[progress - 1] == "." or progress == len(states) - 1:
                    next_progressions[progress] = next_progressions.get(progress, 0) + progressions[progress]

            elif char == ".":
                if states[progress] == "." and progress + 1 < len(states):
                    next_progressions[progress + 1] = next_progressions.get(progress + 1, 0) + progressions[progress]
                if states[progress - 1] == "." or progress == len(states) - 1:
                    next_progressions[progress] = next_progressions.get(progress, 0) + progressions[progress]

            elif char == "#":
                if progress + 1 < len(states) and states[progress] == "#":
                    next_progressions[progress + 1] = next_progressions.get(progress + 1, 0) + progressions[progress]

        progressions = next_progressions
        next_progressions = {}
    sum_of_done_progressions = sum(amount for progress, amount in progressions.items() if progress == len(states) - 1)
    return sum_of_done_progressions


def permutations_for_line(line: str, patterns: tuple[int, ...]) -> int:
    # Optimizations - search can be aborted, if it's impossible to finish
    if sum(patterns) > len([char for char in line if char in ["#", "?"]]):
        return 0
    if sum(patterns) + len(patterns) - 1 > len(line):
        return 0
    idx = 0
    while idx < len(line) and len(patterns) > 0 and patterns[0] <= len(line):
        if line[idx] == ".":
            idx += 1
            continue
        if line[idx] == "#":
            if idx + patterns[0] > len(line):
                # Pattern overshoots line length
                return 0
            if any(char == "." for char in line[idx:idx + patterns[0]]):
                # Next Pattern Rule violated, no valid combo
                return 0
            if idx + patterns[0] < len(line) and line[idx + patterns[0]] == "#":
                return 0
            # if "?" in line[idx:idx + patterns[0] + 1]:
            #     return 1 + permutations_for_line(line[idx + patterns[0] + 1:], patterns[1:])
            return permutations_for_line(line[idx + patterns[0] + 1:], patterns[1:])
        if line[idx] == "?":
            remaining_str = line[idx:]
            q_length = len(list(itertools.takewhile(lambda c: c == "?", remaining_str)))
            if (len(remaining_str) == q_length) or line[idx + q_length] == ".":
                pattern_sets = [patterns[:i] for i in range(len(patterns) + 1)]
                combinations = [
                    arrangements(q_length, p_set) * permutations_for_line(line[idx + q_length:], patterns[len(p_set):])
                    for p_set in pattern_sets]
                # print(f"Searched {line} for {patterns} -> {sum(combinations)}")
                return sum(combinations)
            if line[idx + q_length] == "#":
                # ?-sequence is followed by #
                return (permutations_for_line(("?" * (q_length - 1)) + "#" + remaining_str[q_length:],
                                              patterns) +
                        permutations_for_line(("?" * (q_length - 1)) + "." + remaining_str[q_length:],
                                              patterns))
    if len(patterns) > 0:
        return 0
    if any(char == "#" for char in line[idx:]):
        return 0
    return 1


@lru_cache(maxsize=None)
def arrangements(amount_q: int, patterns: tuple[int, ...]) -> int:
    if len(patterns) - 1 + sum(patterns) > amount_q:
        return 0
    if amount_q == 0:
        # Maybe should also check for patterns == 0?
        return 0
    if len(patterns) == 0:
        return 1
    if len(patterns) == 1:
        return amount_q - patterns[0] + 1
    return sum(arrangements(amount_q - i, patterns[1:]) for i in range(patterns[0] + 1, amount_q))


def run_with_log(i, data):
    line, pattern = data
    result = permutations_for_line(line, pattern)
    print(f"Finished line {i}:\t{line}")
    return result


def possible_patterns(line: str) -> Generator:
    """ Generates all possible variants of `line` replacing each `?` with either `.` or `#`. """
    replacement_chars = [".", "#"]
    char_possibilities = ((replacement_chars if char == "?" else [char]) for char in line)
    return ("".join(chars) for chars in itertools.product(*char_possibilities))


def pattern_to_regex(pattern: str | tuple[int, ...]) -> re.Pattern:
    if isinstance(pattern, str):
        pattern = tuple(pattern.strip().split(","))
    # Build one '#{x}' per number in pattern, which indicates the amount subsequent #-characters.
    # Separate them with at least 1 dot using "\.+" and set any amount of dots before and after the regex with "\.*".
    regex_str = r"^\.*" + r"\.+".join(f'#{{{amount}}}' for amount in pattern) + r"\.*$"
    return re.compile(regex_str)


def count_valid_patterns(lines: Iterable[str], regex: re.Pattern) -> int:
    return sum(1 for line in lines if regex.match(line))


def guess_next_char2(line: str, pattern: str | tuple[int, ...], pattern_index: int = 0,
                     start_buffer: list[str] = None) -> list[str]:
    if isinstance(pattern, str):
        pattern = tuple(int(x) for x in pattern.strip().split(","))
    str_buffer = start_buffer if start_buffer else []
    char_iter = iter(line)
    for char in char_iter:
        # Check if it is even possible to finish this
        # Amount of #/? chars to fulfill remaining patters
        if sum(1 for char in line[len(str_buffer):] if char != ".") < sum(pattern[pattern_index:]):
            return []
        # Amount of ?/# chars, plus their separating "."-characters must be at least the remaining amount of chars
        if (sum(pattern[pattern_index:]) + len(pattern[pattern_index:]) - 1) > len(line) - len(str_buffer):
            return []
        if char == ".":
            str_buffer.append(".")
        elif char == "#":
            # If a #-character is found, this is the definite start of a #-sequence.
            # Append the initial # to the buffer, then advance the iterator for the amount of characters
            # the pattern demands. If ?-character are in the way, they can safely be assumed to be a #-character.
            str_buffer.append("#")
            # ORDER OF zip-ARGUMENTS IS IMPORTANT. When the length limit is reached, we do not want to pop an item
            # off the char_iter. However, that happens, when char_iter is the first iterable.
            # zip() apparently queries them in order and terminates when the first iterable terminates.
            # For our purposes, we need char_iter to NOT be queried, when the range(hash_length) terminates.
            next_chars = [c for _, c in zip(range(pattern[pattern_index] - 1), char_iter)]
            # If any of those following chars that are supposed to be #-chars or ?-chars (which will become "#")
            # is a "."-character, this combination is invalid, since it doesn't fulfill the pattern.
            # The same goes, if there are fewer characters in next_chars, than the pattern demands.
            if len(next_chars) < (pattern[pattern_index] - 1) or any(c == "." for c in next_chars):
                return []
            str_buffer.extend("#" for _ in next_chars)
            # Append the necessary separation dot (even if the original line ends here, this additional dot doesn't
            # hurt, since we're only interested in the amount of options, on the options itself.
            next_char = next(char_iter, None)
            if next_char == "#":
                return []
            if next_char is not None:
                str_buffer.append(".")
            pattern_index += 1
            if pattern_index >= len(pattern):
                # pattern_index is out-of-range, so all patterns are covered
                # If the char_iter contains any more character that aren't "." or "?" (which can be substituted by "."),
                # this combination is invalid, since additional #-character are present.
                last_chars = list(char_iter)
                if any(rc == "#" for rc in last_chars):
                    return []
                solution = "".join(str_buffer + ["."] * len(last_chars))
                return [solution]
                # Final check if the solution actually is one.
                # return [solution] if pattern_to_regex(pattern).match(solution) else []
        elif char == "?":
            # If any character in the line is unknown, we create 2 branches, guessing either . or #, by recursion.
            # We instantly return the combination of both guesses.
            last_chars = list(char_iter)
            hash_guess = guess_next_char("".join(str_buffer + ["#"] + last_chars), pattern,
                                         pattern_index=pattern_index,
                                         start_buffer=list(str_buffer))
            period_guess = guess_next_char("".join(str_buffer + ["."] + last_chars), pattern,
                                           pattern_index=pattern_index,
                                           start_buffer=list(str_buffer))
            return hash_guess + period_guess
    return []


def guess_next_char(line: str, pattern: str | tuple[int, ...], pattern_index: int = 0,
                    start_buffer: list[str] = None) -> list[str]:
    # For each number in the pattern
    # Find first # or ?
    # On #: Count #'s until number is reached, skip over next ".", continue/repeat
    # On ?: Replace with . or #, then call this function recursively with the guess
    #   -> summarize both returned lists
    if isinstance(pattern, str):
        pattern = tuple(int(x) for x in pattern.strip().split(","))
    str_buffer = start_buffer if start_buffer else []
    char_iter = iter(line)
    for pattern_index, hash_length in enumerate(pattern[pattern_index:], start=pattern_index):
        for char_index, char in enumerate(char_iter):
            if char == ".":
                str_buffer.append(".")
            elif char == "#":
                # If a #-character is found, this is the definite start of a #-sequence.
                # Append the initial # to the buffer, then advance the iterator for the amount of characters
                # the pattern demands. If ?-character are in the way, they can safely be assumed to be a #-character.
                str_buffer.append("#")
                # ORDER OF zip-ARGUMENTS IS IMPORTANT. When the length limit is reached, we do not want to pop an item
                # off the char_iter. However, that happens, when char_iter is the first iterable.
                # zip() apparently queries them in order and terminates when the first iterable terminates.
                # For our purposes, we need char_iter to NOT be queried, when the range(hash_length) terminates.
                next_chars = [c for _, c in zip(range(hash_length - 1), char_iter)]
                # If any of those following chars that are supposed to be #-chars or ?-chars (which will become "#")
                # is a "."-character, this combination is invalid, since it doesn't fulfill the pattern.
                # The same goes, if there are fewer characters in next_chars, than the pattern demands.
                if len(next_chars) < (hash_length - 1) or any(c == "." for c in next_chars):
                    return []
                str_buffer.extend("#" for _ in next_chars)
                # Append the necessary separation dot (even if the original line ends here, this additional dot doesn't
                # hurt, since we're only interested in the amount of options, on the options itself.
                next_char = next(char_iter, "..")
                if next_char == "#":
                    return []
                str_buffer.append(".")
                break
            elif char == "?":
                # If any character in the line is unknown, we create 2 branches, guessing either . or #, by recursion.
                # We instantly return the combination of both guesses.
                last_chars = list(char_iter)
                hash_guess = guess_next_char("".join(str_buffer + ["#"] + last_chars), pattern)
                period_guess = guess_next_char("".join(str_buffer + ["."] + last_chars), pattern)
                return hash_guess + period_guess
    # At this point, all pattern are matched and the condition is fulfilled.
    # If the char_iter contains any more character that aren't "." or "?" (which can be substituted by "."),
    # this combination is invalid, since additional #-character are present.
    last_chars = list(char_iter)
    if any(rc == "#" for rc in last_chars):
        return []
    solution = "".join(str_buffer + ["."] * len(last_chars))
    # Final check if the solution actually is one.
    return [solution] if pattern_to_regex(pattern).match(solution) else []


if __name__ == '__main__':
    main()
