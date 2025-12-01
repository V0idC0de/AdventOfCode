def main():
    with open(f'{__file__.split(".")[0]}.txt') as f:
        input_lines = [line.strip() for line in f.readlines()]
    number_rows: list[list[int]] = list(map(lambda line: [int(x) for x in line.strip().split()], input_lines))

    # Part 1
    predictions = [predict_next(numbers) for numbers in number_rows]
    print(f"Challenge 1: {sum(predictions)}")

    # Part 2
    # This asked to extrapolate the number BEFORE the first one, instead of AFTER the last one, using the same logic.
    # However, this effectively is just a reversal of logic and allows to easily calculate this by re-using part 1.
    # Reversing the values of each line of values converts this problem to the problem already solved in part 1.
    predictions = [predict_next(list(reversed(numbers))) for numbers in number_rows]
    print(f"Challenge 2: {sum(predictions)}")


def predict_next(numbers: list[int]) -> int:
    if all(x == 0 for x in numbers):
        return 0
    deltas = [b - a for a, b in zip(numbers, numbers[1:])]
    return numbers[-1] + predict_next(deltas)


if __name__ == '__main__':
    main()
