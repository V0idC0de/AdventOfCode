with open(f'{__file__.split(".")[0]}.txt') as f:
    lines = [l.strip() for l in f.readlines()]

lines = [tuple(line.split(",")) for line in lines]
lines = [tuple(x1.split("-") + x2.split("-")) for x1, x2 in lines]
lines = [(int(x1), int(x2), int(x3), int(x4)) for x1, x2, x3, x4 in lines]

print(f"Part 1: {sum(1 for xstart, xend, ystart, yend in lines if (ystart <= xstart <= xend <= yend) or (xstart <= ystart <= yend <= xend))}")
print(f"Part 2: {sum(1 for xstart, xend, ystart, yend in lines if (ystart <= xstart <= yend) or (ystart <= xend <= yend) or (xstart <= ystart <= xend) or (xstart <= yend <= xend))}")
print(f"Part 2: {sum(1 for xstart, xend, ystart, yend in lines if (ystart <= max(xstart, xend) <= yend) or (xstart <= max(ystart, yend)<= xend))}")