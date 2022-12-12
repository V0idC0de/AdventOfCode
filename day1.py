with open("day1.txt") as f:
    lines = f.readlines()

chunks = "".join(lines).split("\n\n")


def chunk_to_sum(s: str) -> int:
    vals = s.split()
    return sum(int(i) for i in vals)


elves = [chunk_to_sum(s) for s in chunks]

print(f"Part 1: {max(elves)}")
elves.sort(reverse=True)
print(f"Part 2: {sum(elves[:3])}")
