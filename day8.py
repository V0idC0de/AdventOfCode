import itertools
import operator
from functools import reduce
from typing import List

with open(f'{__file__.split(".")[0]}.txt') as f:
    trees = [l.strip("\n") for l in f.readlines()]


def is_tree_visible_from_edge(forest: List[str], row: int, col: int) -> bool:
    directions = [
        [forest[row][i] for i in range(col)],
        [forest[row][i] for i in range(col + 1, len(forest[0]))],
        [forest[i][col] for i in range(row)],
        [forest[i][col] for i in range(row + 1, len(forest))]
    ]
    if any((len(neighbors) == 0) for neighbors in directions):
        # Edge tree
        return True
    return any((forest[row][col] > max(neighbors)) for neighbors in directions)


def view_distance(tree_heights: List, max_height: int) -> int:
    if len(tree_heights) == 0:
        return 0
    for distance, height in enumerate(tree_heights, start=1):
        if int(height) >= int(max_height):
            return distance
    # In case no tree is higher, the distance is counted until it hits the edge.
    # In this case, this is the last known view_distance, from the last iteration.
    return len(tree_heights)


def heights_from_viewpoint(forest: List[str], row: int, col: int) -> List[List[str]]:
    directions = [
        [forest[row][i] for i in range(col)][::-1],  # Reverse to go from coordinates to edge
        [forest[row][i] for i in range(col + 1, len(forest[0]))],
        [forest[i][col] for i in range(row)][::-1],  # Reverse to go from coordinates to edge
        [forest[i][col] for i in range(row + 1, len(forest))]
    ]
    return directions


def scenic_score(forest: List[str], row: int, col: int) -> int:
    tree_heights = heights_from_viewpoint(forest, row, col)
    return reduce(operator.mul,
                  [view_distance(tree_row, int(forest[row][col])) for tree_row in tree_heights])


coordinates = itertools.product(range(len(trees)), range(len(trees[0])))
print(f"Part 1: {sum(1 for row, col in coordinates if is_tree_visible_from_edge(trees, row, col))}")

coordinates = itertools.product(range(len(trees)), range(len(trees[0])))
print(f"Part 2: {max(scenic_score(trees, row, col) for row, col in coordinates)}")
