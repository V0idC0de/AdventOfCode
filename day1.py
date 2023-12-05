with open(f'{__file__.split(".")[0]}.txt') as f:
    input_lines = f.readlines()
    
def digits_from_line(line_text: str) -> int:
    digits: List[str] = list(filter(str.isdigit, line_text))
    return int(f"{digits[0]}{digits[-1]}")

numbers = map(digits_from_line, input_lines)
print(sum(numbers))