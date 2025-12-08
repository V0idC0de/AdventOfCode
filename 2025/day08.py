import itertools as it
import math
import time
from collections import defaultdict
from typing import Iterable

with open(f'{__file__.split(".")[0]}.txt', mode="r") as f:
    input_lines = [l.strip() for l in f.readlines()]


def strs_to_num_tuple(nums: list[str | int]) -> tuple[int, ...]:
    return tuple(int(n) for n in nums)


def vector_distance(vector1: tuple[int, int, int], vector2: tuple[int, int, int]) -> float:
    return sum((a - b) ** 2 for a, b in zip(vector1, vector2)) ** 0.5


def build_n_connections(connections: Iterable[tuple[tuple[int, int, int], tuple[int, int, int]]],
                        n: int) -> list[set[tuple[int, int, int]]]:
    circuits: dict[tuple[int, int, int], set[tuple[int, int, int]]] = defaultdict(set)

    for i, (box1, box2) in zip(range(n), connections):
        b1_circut, b2_circut = circuits[box1], circuits[box2]
        if b1_circut is not b2_circut:
            combined_circuit = b1_circut | b2_circut | {box1, box2}
            for box in combined_circuit:
                circuits[box] = combined_circuit

    # Deduplicate circuits which are identical objects (= literally the very same set object
    circuit_ids = {id(circuit): circuit for circuit in circuits.values()}
    return list(circuit_ids.values())


def connect_until_one_circuit(connections: Iterable[tuple[tuple[int, int, int], tuple[int, int, int]]],
                              circuit_size: int) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    circuits: dict[tuple[int, int, int], set[tuple[int, int, int]]] = defaultdict(set)

    for box1, box2 in connections:
        b1_circut, b2_circut = circuits[box1], circuits[box2]
        if b1_circut is not b2_circut:
            combined_circuit = b1_circut | b2_circut | {box1, box2}
            for box in combined_circuit:
                circuits[box] = combined_circuit
            # Stop, if we found the big circuit
            if len(combined_circuit) >= circuit_size:
                return box1, box2
    raise RuntimeError("Could not connect all boxes into one circuit")


if __name__ == "__main__":
    split_nums_by_row = map(lambda s: s.split(","), input_lines)
    int_tuples = map(strs_to_num_tuple, split_nums_by_row)
    boxes = list(int_tuples)

    start_time = time.perf_counter_ns()

    distances = {(v1, v2): vector_distance(v1, v2) for v1, v2 in it.combinations(boxes, 2)}
    sorted_distances = sorted(distances.items(), key=lambda item: item[1])
    sorted_connections = [pair for pair, dist in sorted_distances]

    # Part 1
    circuits = build_n_connections(sorted_connections, n=len(boxes))
    sorted_circuit_lens = sorted(circuits, key=len, reverse=True)
    print(f"Part 1: {math.prod(map(len, sorted_circuit_lens[:3]))}")

    # Part 2
    box1, box2 = connect_until_one_circuit(sorted_connections, circuit_size=len(boxes))
    print(f"Part 2: {box1[0] * box2[0]}")

    end_time = time.perf_counter_ns()
    print(f"Time: {(end_time - start_time) / 1_000_000:.3f} ms")
