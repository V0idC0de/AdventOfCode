import operator
from functools import reduce

with open(f'{__file__.split(".")[0]}.txt') as f:
    commands = [l.strip("\n") for l in f.readlines()]

# Purge "$ ls" as it does nothing
commands = [cmd for cmd in commands if cmd != "$ ls"]
# Ignore the first "cd /" as it messes with the logic - manually adding / is easier
commands = commands[1:]

cwd = "/"
dirs = ["/"]

files = {}

for line in commands:
    if line.startswith("$ cd"):
        # Append the cd-target to pwd
        if line[5:] == "..":
            # Slice off the last 2 slashes and everything in between it (= last directory).
            # Then ensure the path ends with a string to maintain a good state.
            cwd = cwd.rsplit("/", maxsplit=2)[0] + "/"
        else:
            # Append cd-target to pwd and add to known dirs
            cwd += f'{line[5:]}/'
            dirs.append(cwd)
    elif line.startswith("dir "):
        dirs.append(f'{cwd}{line[5:]}/')
    else:
        # Must be a size followed by a filename (the latter is irrelevant for now)
        size, filename = line.split(maxsplit=1)
        files[f'{cwd}{filename}'] = int(size)


def dir_size(d: str) -> int:
    return sum(fsize for fname, fsize in files.items() if fname.startswith(d))


part1 = reduce(operator.add,
               filter(lambda fsize: fsize <= 100000,
                      map(dir_size, dirs)))
print(f"Part 1: {part1}")

# Part 2
# Get all dirs mapped to their size
dir_sizes = {d: dir_size(d) for d in dirs}
total_space = 70000000
required_space = 30000000
used_space = dir_sizes["/"]
space_to_make = required_space + used_space - total_space

deletion_candidates = filter(lambda item: item[1] >= space_to_make,
                             dir_sizes.items())
smallest_candidate, smallest_size = min(deletion_candidates, key=lambda item: item[1])

print(f'Part 2: Directory "{smallest_candidate.split("/")[-2]}" with size {smallest_size} at "{smallest_candidate}"')
