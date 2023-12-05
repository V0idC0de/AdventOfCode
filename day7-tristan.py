with open(f'{__file__.split(".")[0]}.txt') as f:
    lines = [l.strip("\n") for l in f.readlines()]

star_one = 0
star_two = 0
cwd = []
filesystem = {}


def shell(command, directory):
    if command == 'ls':
        pass
    if command == 'cd':
        if directory == '..':
            cwd.pop()
        else:
            cwd.append(directory)


def set_file_size(path, size):
    directory_tree = ''
    for directory in path:
        directory_tree = directory_tree + directory
        filesystem[directory_tree] = filesystem.get("directory_tree", 0) + int(size)


for line in lines:
    line = line.split()
    if line[0] == "$":
        shell(line[1], line[-1])
    else:
        if line[0] == "dir":
            pass
        else:
            current_file = "/".join(cwd) + "/" + line[1]
            filesystem.update({current_file: line[0]})
            set_file_size(cwd, line[0])

for path, size in filesystem.items():
    if size == 'dir':
        pass
    elif int(size) <= 100000:
        star_one += int(size)

print(filesystem)

print("Result for Star 1: ", star_one)
print("Result for Star 2: ", star_two)
