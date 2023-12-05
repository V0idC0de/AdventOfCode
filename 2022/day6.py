with open(f'{__file__.split(".")[0]}.txt') as f:
    line = [l.strip("\n") for l in f.readlines()][0]


def find_unique_sequence_index(text: str, length: int) -> int:
    for i in range(len(text)):
        chunk = text[i:i + 4]
        if len(chunk) == len(set(chunk)):
            return i + length


print(f"Part 1: {find_unique_sequence_index(line, 4)}")
print(f"Part 2: {find_unique_sequence_index(line, 14)}")