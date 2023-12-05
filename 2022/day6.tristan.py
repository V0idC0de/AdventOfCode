with open(f'{__file__.split(".")[0]}.txt') as f:
    line = [l.strip("\n") for l in f.readlines()][0]

star_one = 0
star_two = 0

cursor = []

for start_of_header, char in enumerate(line):
    if len(list(dict.fromkeys(cursor))) == 4 and len(cursor) == 4:
        star_one = start_of_header
        break

    cursor.append(char)

    if len(cursor) == 5:
        del cursor[0]

print("Result for Star 1: ", star_one)
print("Result for Star 2: ", star_two)