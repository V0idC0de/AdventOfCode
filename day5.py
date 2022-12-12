from collections import defaultdict
from copy import deepcopy
from typing import List, Dict

with open(f'{__file__.split(".")[0]}.txt') as f:
    lines = [l.strip("\n") for l in f.readlines()]

state = lines[:8]
operations = lines[10:]

state_lists: Dict[str, List] = defaultdict(lambda: list())

for line in reversed(state):
    for state_key, col_index in enumerate(range(1, len(line), 4), start=1):
        if s := line[col_index].strip():
            state_lists[str(state_key)].append(s)

state_lists2: Dict[str, List] = deepcopy(state_lists)

# Process instructions - Part 1
for instruction in operations:
    _, iterations, _, src, _, dest = instruction.split()
    for _ in range(int(iterations)):
        state_lists[dest].append(state_lists[src].pop())

print(f'Part 1: {"".join([l[-1] for l in state_lists.values()])}')

# ## Part 2
# Process instructions - Part 2
for instruction in operations:
    _, height, _, src, _, dest = instruction.split()
    height = int(height)
    state_lists2[dest] += state_lists2[src][-height:]
    state_lists2[src] = state_lists2[src][:-height]

print(f'Part 2: {"".join([l[-1] for l in state_lists2.values()])}')

"""
{0: ['R', 'G', 'J', 'B', 'T', 'V', 'Z'], 
1: ['J', 'R', 'V', 'L'], 
2: ['S', 'Q', 'F'], 
3: ['Z', 'H', 'N', 'L', 'F', 'V', 'Q', 'G'], 
4: ['R', 'Q', 'T', 'J', 'C', 'S', 'M', 'W'], 
5: ['S', 'W', 'T', 'C', 'H', 'F'], 
6: ['D', 'Z', 'C', 'V', 'F', 'N', 'J'], 
7: ['L', 'G', 'Z', 'D', 'W', 'R', 'F', 'Q'], 
8: ['J', 'B', 'W', 'V', 'P']})"""
