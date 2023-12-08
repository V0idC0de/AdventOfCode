import itertools
import math
import time
from collections.abc import Generator


def graph_steps(node_map: dict[str, dict[str, str]],
                direction_sequence: str,
                start: str = "AAA",
                end: str | None = None) -> Generator[str]:
    """
    Returns a Generator producing the steps which are taken.

    :param node_map: Graph representing the nodes, as well as their directions and next nodes
    :param direction_sequence: String of "R" and "L", representing the direction sequence to take. Will be cycled.
    :param start: Node to start at. Default is "AAA"
    :param end: Last node in the sequence. Once reached, the Generator will exhaust.
        Defaults to None, producing steps until no more steps are available.
    :return:
    """
    location = start
    for direction in itertools.cycle(direction_sequence):
        node = node_map.get(location)
        if location == end:
            return
        if node is not None:
            location = node[direction]
            yield location


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]

    walk_sequence = input_lines[0].strip()
    # Store each node as a dict-key and the value is a dict with the nodes for directions "R" and "L"
    graph = {l[:3]: {"L": l[7:10], "R": l[12:15]} for l in input_lines[2:]}

    # Part 1
    steps = sum(1 for _ in graph_steps(graph, walk_sequence, start="AAA", end="ZZZ"))
    print(f"Challenge 1: {steps}")

    # Part 2
    # As an exhaustive search turned out to be too much (see line 52+), hence some mathematical approach was required.
    # The paths each explorer takes have to loop, otherwise the maximum steps required for the solution are twice the
    # length of the node list - which is not the case, since the exhaustive search would've found it then.
    # The path indeed are cyclic and have exactly one destination location (node ending with "Z").
    # So we're looking for the cycle in which "coincidentally" all cycles end up at their destination node.
    # This is effectively looking for a common multiple of all of explorer's cycle sizes - the least common multiple.
    # So let's start by enumerating the paths each explorer takes until it loops.
    start_nodes = [node for node in graph.keys() if node.endswith("A")]
    cycles = [get_cycle(graph, walk_sequence, start=node) for node in start_nodes]
    # cycles already contains the loop only. For some paths it takes a few steps to get to the looping section.
    # This requires shifting the list of nodes a bit, to account for these "introduction steps" that happen only once.
    # Funny enough, this causes the destination node to be the very first node on each path - what a "coincidence"!
    # So we now just take the length of each cycle (= amount of steps to end up at the first node again, which is the
    # destination node) and calculate the LEAST COMMON MULTIPLIER of all those to find the amount of steps required
    # to end up at the start of all path's loop at the same time.
    # FUN FACT: The sum of cycle length and "introduction steps to reach the cycle" is a prime-number for all paths.
    least_common_multiple = math.lcm(*(len(cycle) for cycle in cycles))
    # Magnitude is ~10**13, which explains why the exhaustive search didn't finish (and wouldn't have had anytime soon)
    print(f"Challenge 2: {least_common_multiple}")
    return

    # noinspection PyUnreachableCode
    # This code works for smaller solutions, but just like day 6, takes an enormous amount of time with puzzle input.
    # I liked the generator-based approach and there are quite cool Python features at display, so I leave it in here.

    start_nodes = [node for node in graph.keys() if node.endswith("A")]
    # Create a generator for each of the starting nodes, which will produce the steps, starting at that node
    explorers = (graph_steps(graph, walk_sequence, start=node) for node in start_nodes)
    # Place all generators in zip(), so in each iteration, we get a tuple containing the new locations of the explorers.
    # Using takewhile() we'll produce tuples, as long as the locations do NOT all end with "Z". If they do, we're done.
    until_all_z_iter = itertools.takewhile(lambda locs: not all(loc.endswith("Z") for loc in locs), zip(*explorers))
    # Count the steps in a memory-friendly way using sum(1 for ...), adding one, since the last step is dropped,
    # due to takewhile's condition failing when we reach locations all ending in "Z", omitting that step in the process.
    steps = sum(1 for _ in until_all_z_iter) + 1
    print(f"Challenge 2: {steps}")


def get_cycle(node_map: dict[str, dict[str, str]], direction_sequence: str, start: str = "AAA") -> list[str]:
    """
    Iterates through graph_steps() until a cycle is detected. Returns all nodes that are part of the cycle,
    adjusted by the amount of steps required to reach the start of the cycle (cyclic shift-right of the list).
    """
    direction_iter = itertools.cycle(direction_sequence)
    next(direction_iter)
    steps_iter = zip(graph_steps(node_map, direction_sequence, start=start),
                     itertools.cycle(range(len(direction_sequence))))
    cycle: list[tuple[str, int]] = [(start, None)]
    for step in steps_iter:
        if step in cycle:
            # Loop detected - isolate the loop
            steps_to_loop = cycle.index(step)
            loop_only = [loc for loc, direction in cycle][steps_to_loop:]
            # The loop has a couple steps to get into it. Shift the loop start to account for that.
            return loop_only[-steps_to_loop:] + loop_only[:-steps_to_loop]
        cycle.append(step)


if __name__ == '__main__':
    start_time = time.time_ns()
    main()
    print(f"Time: {(time.time_ns() - start_time) / 10 ** 9:.5f}s")
