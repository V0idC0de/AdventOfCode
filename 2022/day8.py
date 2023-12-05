import itertools
import operator
from functools import reduce
from typing import List

with open(f'{__file__.split(".")[0]}.txt') as f:
    trees = [l.strip("\n") for l in f.readlines()]


def is_tree_visible_from_edge(forest: List[str], row: int, col: int) -> bool:
    """
    For the given `forest`, checks whether the trees in between the tree at `row`/`col` and any of the edges
    are all smaller than the tree itself (i.e. whether the tree is visible from any edge).
    """
    directions = [
        [forest[row][i] for i in range(col)],
        [forest[row][i] for i in range(col + 1, len(forest[0]))],
        [forest[i][col] for i in range(row)],
        [forest[i][col] for i in range(row + 1, len(forest))]
    ]
    if any((len(neighbors) == 0) for neighbors in directions):
        # Tree is already at an edge, if there are no trees in one of the directions, so it's definitely visible.
        return True
    return any((forest[row][col] > max(neighbors)) for neighbors in directions)


def view_distance(tree_heights: List, max_height: int) -> int:
    """
    Iterates `tree_heights` and counts until the n-th element is hit, whose value is equal or greater than `max_height`.
    :return: Amount of consecutive elements in `tree_heights` (starting at index 0), less than `max_height`.
        The final element is included, as that last tree is still visible, despite being higher.
        If no element of `tree_heights` is greater than or equal to `max_height`, the maximum of len(tree_heights) is
        returned, as all trees can be seen then.
    """
    if len(tree_heights) == 0:
        return 0
    for distance, height in enumerate(tree_heights, start=1):
        if int(height) >= int(max_height):
            return distance
    # In case no tree is higher, the distance is counted until it hits the edge.
    # In this case, this is the last known view_distance, from the last iteration.
    return len(tree_heights)


def heights_from_viewpoint(forest: List[str], row: int, col: int) -> List[List[str]]:
    """
    For the `forest`, lists the height for each tree between the given tree at `row`/`col`,
    starting at that tree and going towards the edges. Each direction is listed separately as a list.
    :return: List of lists, each inner list representing the heights of trees visible in one of the directions.
    """
    directions = [
        [forest[row][i] for i in range(col)][::-1],  # Reverse to go from coordinates to edge
        [forest[row][i] for i in range(col + 1, len(forest[0]))],
        [forest[i][col] for i in range(row)][::-1],  # Reverse to go from coordinates to edge
        [forest[i][col] for i in range(row + 1, len(forest))]
    ]
    return directions


def scenic_score(forest: List[str], row: int, col: int) -> int:
    """
    Calculates the scenic score for a given tree at `row`/`col` in the forest, as given by the challenge description.
    """
    tree_heights = heights_from_viewpoint(forest, row, col)
    return reduce(operator.mul,
                  [view_distance(tree_row, int(forest[row][col])) for tree_row in tree_heights])


coordinates = itertools.product(range(len(trees)), range(len(trees[0])))
print(f"Part 1: {sum(1 for row, col in coordinates if is_tree_visible_from_edge(trees, row, col))}")

coordinates = itertools.product(range(len(trees)), range(len(trees[0])))
print(f"Part 2: {max(scenic_score(trees, row, col) for row, col in coordinates)}")
