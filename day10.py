with open(f'{__file__.split(".")[0]}.txt') as f:
    operations = [l.strip("\n") for l in f.readlines()]

# x_deltas is a list of lists, collecting the changes to the signal for each cycle, as given by the input operations.
# "noop" uses one cycle, thus only [0], while "addx" uses 2, but the first cycle doesn't change anything.
# This list of lists is then flattened to one complete list of deltas, where each element represents one cycle.
# Starting with a [1] element, since the start value of X is 1.
x_deltas = sum([[0] if op == "noop" else [0, int(op.split()[-1])] for op in operations], [1])

# Sum up all deltas from the start to the cycle we want to know the "signal strength" of.
# Normally, we'd have to shift the index back by 1, as the cycle numbers are 1-based and list indexes are 0-based,
# however, by adding the start value "1" as delta, this equalizes, since the start value is technically not a cycle.
# Still, the task says to measure DURING the 20th(, ...) cycle, which means that the operation happening is not completed
# effectively asking for the cycle result before this cycle (shifting index to -1).
# End-indexes are exclusive, so we just add one to the slicing-index, making it "i - 1 + 1" = i.
print(f'Part 1: {sum(sum(x_deltas[:i]) * i for i in range(20, len(x_deltas), 40))}')
