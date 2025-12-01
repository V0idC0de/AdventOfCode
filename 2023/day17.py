from collections import defaultdict

directions = {
    "|": ((-1, 0, "-"), (1, 0, "-")),
    "-": ((0, -1, "|"), (0, 1, "|"))
}
Node = tuple[tuple[int, int], str]


def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = tuple(line.strip() for line in f.readlines())

    # Part 1
    part1 = dijkstra(input_lines, 1, 3)
    print(f"Challenge 1: {part1}")

    # Part 2
    part2 = dijkstra(input_lines, 4, 10)
    print(f"Challenge 2: {part2}")


def dijkstra(grid: tuple[str, ...], min_move: int, max_move: int) -> int:
    # When calling for a field that doesn't exist, just return a super-high number.
    # That way, we do not need to enumerate everything in advance.
    # Besides that, this dict stores the heat-loss caused to reach a certain field.
    # The direction this field will be left with is important, since depending on the path,
    # we might not be allowed to leave a field in a certain direction.
    node_metrics = defaultdict(lambda: 10 ** 7)
    # Set starting nodes
    node_metrics[((0, 0), "|")] = 0
    node_metrics[((0, 0), "-")] = 0

    # Store all visited nodes, according to Dijkstra, along with our target nodes
    visited_nodes: set[Node] = set()
    target_nodes = [((len(grid) - 1, len(grid[0]) - 1), "|"),
                    ((len(grid) - 1, len(grid[0]) - 1), "-")]

    # This is an alternative loop condition that explores all nodes. However, if Dijkstra finds the target node,
    # its value is already optimal, since we're always exploring the nodes with the least heat-loss first.
    # ## Loop as long as there are node which are unknown.
    # while unknown_nodes := set(node_metrics.keys()).difference(visited_nodes):

    # ## Loop as long as there aren't any of the target nodes in the known_nodes
    while not any(t_node in visited_nodes for t_node in target_nodes):
        # Create a set of all nodes, not yet explored and find the one with the minimum heat-loss
        unknown_nodes = set(node_metrics.keys()).difference(visited_nodes)
        current_node = min(unknown_nodes, key=lambda node: node_metrics[node])
        coords, next_fork = current_node
        # Get all nodes that could result from a movement in the given directions.
        # This will assume that we're moving all possible amounts of steps in one direction and then turn 90°
        for next_node, delta_distance in next_nodes(grid, coords, next_fork, min_move, max_move).items():
            # If we found a better way to a node than previously known, save it
            if node_metrics[current_node] + delta_distance < node_metrics[next_node]:
                node_metrics[next_node] = node_metrics[(coords, next_fork)] + delta_distance
            # Mark the current node as visited, so we don't explore it again
            visited_nodes.add(current_node)

    least_heat_loss = min(node_metrics[target_nodes[0]], node_metrics[target_nodes[1]])
    return least_heat_loss


def next_nodes(grid: tuple[str, ...],
               current_node: tuple[int, int],
               next_directions: str,
               min_move: int = 1,
               max_move: int = 3) -> dict[Node, int]:
    """
    Generates a `dict` of all nodes that can be reached from `current_node`, be moving anything between `min_move` and
    `max_move` steps. The nodes are mapped to the heat-loss incurred by reaching them from `current_node`.
    Nodes which are out-of-bounds are excluded automatically. The next nodes will have the other direction,
    which is not `next_direction`, since we assume that after going the steps, the path turns 90°.
    """
    next_steps: dict[Node, int] = {}
    # Go through the tuples, that point to the directions the step(s) should go. The Tuples are normal vectors.
    for dir_tuple in directions[next_directions]:
        delta_y, delta_x, next_fork = dir_tuple
        # There may be multiple distance we could go before turning. (1 step, 2 steps, etc.)
        for factor in range(min_move, max_move + 1):
            # Calculate coordinates of the target node that is reached after the steps, then check if it's in-bounds.
            next_y, next_x = current_node[0] + delta_y * factor, current_node[1] + delta_x * factor
            if 0 <= next_x < len(grid[0]) and 0 <= next_y < len(grid):
                # While making `factor` steps, heat-loss from the fields passed is collected.
                # Go through the range of coordinates which we passed to calculate heat-loss while going to the field.
                heat_loss = 0
                if delta_y != 0:
                    steps_to_old_node = range(next_y, current_node[0], 1 if next_y <= current_node[0] else -1)
                    heat_loss = sum(int(grid[i][next_x]) for i in steps_to_old_node)
                elif delta_x != 0:
                    steps_to_old_node = range(next_x, current_node[1], 1 if next_x <= current_node[1] else -1)
                    heat_loss = sum(int(grid[next_y][i]) for i in steps_to_old_node)
                # Store the reached node and the incurred heat-loss in the `dict` of next possible nodes
                next_steps[((next_y, next_x), next_fork)] = heat_loss
            else:
                # Steps taken in the direction only get bigger. Once out of bound, all following steps will be OoB, too.
                break
    return next_steps


if __name__ == '__main__':
    main()
