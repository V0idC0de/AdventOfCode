import itertools
import re
import time
from collections.abc import Iterable
from multiprocessing.pool import Pool
from typing import Generator


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]
    lines = [line.split() for line in input_lines]

    # Part 1
    # possibilities_per_line = ((possible_patterns(line), pattern_to_regex(pattern)) for line, pattern in lines)
    # options_per_line = (count_valid_patterns(s, regex) for s, regex in possibilities_per_line)
    options_per_line = (guess_next_char(s, pattern) for s, pattern in lines)
    print(f"Challenge 1: {sum(len(options) for options in options_per_line)}")

    # Part 2
    lines = [("?".join([line] * 5), ",".join([pattern] * 5)) for line, pattern in lines]
    start_time = time.time()
    with Pool() as pool:
        possibilities_per_line = pool.starmap(run_with_log, lines, chunksize=5)
    # for line, pattern in lines:
    #     print(f"Working on line after {time.time() - start_time}s")
    #     possibilities_per_line.append(guess_next_char(line, pattern))
    print(f"Challenge 2: {sum(len(line) for line in possibilities_per_line)}")
    print(f"Done after {time.time() - start_time} seconds")


def run_with_log(line, pattern):
    result = guess_next_char2(line, pattern)
    print(f"Finished line: {line}")
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
                next_char = next(char_iter, ".")
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
