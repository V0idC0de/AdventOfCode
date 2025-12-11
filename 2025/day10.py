import collections
import itertools
import itertools as it
import operator
from functools import reduce
from queue import Queue

with open(f'{__file__.split(".")[0]}.txt', mode="r") as f:
    # Leading and trailing spaces matter in this challenge, so do not strip() lines here
    input_lines = [l.strip() for l in f.readlines()]


def nums_to_mask(nums: tuple[int, ...], total_length: int) -> int:
    return sum(1 << (total_length - 1 - n) for n in nums)


def light_switch_buttons(line: str) -> tuple[int, ...]:
    light_chars = line[line.index("[") + 1:line.index("]")]
    lights = sum(1 << (len(light_chars) - 1 - i) for i, c in enumerate(light_chars) if c == "#")
    joltages = tuple(int(s) for s in line[line.index("{") + 1:line.index("}")].split(","))
    connection_blocks = (block.strip("()") for block in line[line.index(" ") + 1:line.index("{") - 1].split())
    connections = tuple(tuple(map(int, block.split(","))) for block in connection_blocks)
    # Bit-masks for each button
    btn_masks: tuple[int, ...] = tuple(nums_to_mask(btn, len(light_chars)) for btn in connections)
    btn_presses = it.chain.from_iterable(it.combinations(btn_masks, r=n) for n in range(1, len(btn_masks) + 1))
    for press_combination in btn_presses:
        result = reduce(operator.xor, press_combination, lights)
        if result == 0:
            return press_combination
    raise RuntimeError("No solution found")


def joltage_buttons_slow(line: str) -> tuple[tuple[int, ...], ...]:
    target_joltages = tuple(int(s) for s in line[line.index("{") + 1:line.index("}")].split(","))
    connection_blocks = (block.strip("()") for block in line[line.index(" ") + 1:line.index("{") - 1].split())
    connections = tuple(tuple(map(int, block.split(","))) for block in connection_blocks)
    btn_presses = it.chain.from_iterable(
        it.combinations_with_replacement(connections, r=n) for n in it.count(max(target_joltages)))
    for press_combination in btn_presses:
        raised_joltage_indices = it.chain.from_iterable(press_combination)
        counted_increases: dict[int, int] = collections.Counter(raised_joltage_indices)
        joltage_sum = tuple(counted_increases.get(i, 0) for i in range(len(target_joltages)))
        if joltage_sum == target_joltages:
            return press_combination
    raise RuntimeError("No solution found")


def joltage_buttons(line: str) -> int:
    target_joltages = tuple(int(s) for s in line[line.index("{") + 1:line.index("}")].split(","))
    connection_blocks = (block.strip("()") for block in line[line.index(" ") + 1:line.index("{") - 1].split())
    connections = tuple(tuple(map(int, block.split(","))) for block in connection_blocks)
    return eliminate_slot_big_jump_first(target_joltages, frozenset(connections), 0)


def eliminate_slot_big_jump_first(joltages: tuple[int, ...], buttons: frozenset[tuple[int, ...]],
                                  presses_taken: int) -> int:
    min_idx = joltages.index(min(filter(lambda x: x > 0, joltages)))
    # Check if all joltages that need to be configured, have a button left, which configures them.
    joltages_to_configure = (idx for idx, j in enumerate(joltages) if j > 0)
    if not all(idx in it.chain.from_iterable(buttons) for idx, j in enumerate(joltages_to_configure) if j > 0):
        return 0
    # If no buttons are available, this path is invalid, thus return 0, to not contribute to the sum.
    possible_buttons = list(filter(lambda btn: min_idx in btn, buttons))
    if len(possible_buttons) == 0:
        return 0
    button_to_press = max(possible_buttons, key=len)
    # Press maximum amount of times, down to a single press, testing each amount.
    # If solution is found, return immediately with the amount of presses taken.
    # If no solution is found, but nothing is negative yet (valid button press),
    #     add the presses takes (i) and recurse.
    #     Remove the pressed button from the available buttons, so others are tried.
    # If no available button can be pressed without going negative (end of loop), return 0, as this is a failed path.
    for i in range(joltages[min_idx], -1, -1):
        new_joltages = tuple(x - (i if idx in button_to_press else 0) for idx, x in enumerate(joltages))
        if all(x == 0 for x in new_joltages):
            return presses_taken + i
        if all(x >= 0 for x in new_joltages):
            new_buttons: frozenset[tuple[int, ...]] = frozenset(
                btn for btn in buttons
                if btn != button_to_press and all(new_joltages[idx] > 0 for idx in btn)
            )
            presses = eliminate_slot_big_jump_first(joltages=new_joltages, buttons=new_buttons,
                                                    presses_taken=presses_taken + i)
            if presses > 0:
                return presses
    # No button can be pressed without going negative
    return 0


if __name__ == "__main__":
    # Part 1
    button_presses = sum(len(light_switch_buttons(line)) for line in input_lines)
    print(f"Part 1: {button_presses}")

    # Part 2
    # joltage_buttons(input_lines[0])
    # exit(0)
    button_presses, results = itertools.tee(joltage_buttons(line) for line in input_lines)
    for i, presses in enumerate(button_presses):
        print(f"Line {i + 1}: {presses} button presses")
    print(f"Part 2: {sum(results)} button presses")
