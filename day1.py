with open(f'{__file__.split(".")[0]}.txt') as f:
    input_lines = [l.strip() for l in f.readlines()]

def p1_digits_from_line(line_text: str) -> int:
    # Simple number finder for part 1
    digits: List[str] = list(filter(str.isdigit, line_text))
    return int(f"{digits[0]}{digits[-1]}")

def p2_digits_from_line(line_text: str) -> int:
    # Finds first and last occurrences of valid search terms for part 2
    search_terms = {
        "one": 1, "1": 1,
        "two": 2, "2": 2,
        "three": 3, "3": 3,
        "four": 4, "4": 4,
        "five": 5, "5": 5,
        "six": 6, "6": 6,
        "seven": 7, "7": 7,
        "eight": 8, "8": 8,
        "nine": 9, "9": 9,
    }
    # Find lowest index of any digit occurrence (first digit)
    search_term_indices = [(line_text.find(text), value) for text, value in search_terms.items() if line_text.find(text) >= 0]
    min_index, min_index_value = min(search_term_indices)
    # Find highest index of any digit occurrence (last digit)
    search_term_indices = [(line_text.rfind(text), value) for text, value in search_terms.items() if line_text.rfind(text) >= 0]
    max_index, max_index_value = max(search_term_indices)
    # min_index_value is the first (= higher) digit, so it's multiplied by 10, while the last (= lower) digit is just added.
    # Example: 5 and 2 becomes 50 + 2
    return min_index_value * 10 + max_index_value


part1_sum = sum(map(p1_digits_from_line, input_lines))
print(f"Challenge 1: {part1_sum}")

part2_sum = sum(map(p2_digits_from_line, input_lines))
print(f"Challenge 2: {part2_sum}")
