from collections import namedtuple

with open(f'{__file__.split(".")[0]}.txt') as f:
    input_lines = [l.strip() for l in f.readlines()]

Dices = namedtuple("Dices", "red green blue")

def line_to_games(line: str) -> list[str]:
    game_lines = [game_line.strip() for game_line in line.split(";")]
    return [game_to_dices(game_line) for game_line in game_lines]

def game_to_dices(line: str) -> Dices:
    amount_color_texts: list[str] = [s.strip() for s in line.split(",")]
    color_to_amount = {}
    for dice in amount_color_texts:
        amount, color = dice.split()
        color_to_amount[color] = int(amount)
    return Dices(color_to_amount.get("red", 0),
                 color_to_amount.get("green", 0),
                 color_to_amount.get("blue", 0))

# Cut off the "Game 10" text as we don't need that
game_lines = [line.split(":")[-1].strip() for line in input_lines]
total_games: list[list[Dices]] = [line_to_games(line) for line in game_lines]

# Part 1
def game_possible(games: list[Dices], limit: Dices) -> bool:
    return all(dice.red <= limit.red for dice in games) and \
           all(dice.green <= limit.green for dice in games) and \
           all(dice.blue <= limit.blue for dice in games)
           
indexed_games = enumerate(total_games, start=1)
part1_sum = sum(i for i, game in indexed_games if game_possible(game, Dices(12, 13, 14)))
print(f"Challenge 1: {part1_sum}")

# Part 2
def minimum_dices(games: list[Dices]) -> Dices:
    return Dices(max(d.red for d in games),
                 max(d.green for d in games),
                 max(d.blue for d in games))

def dice_power(dice: Dices) -> int:
    return dice.red * dice.blue * dice.green

minimum_list = map(minimum_dices, total_games)
dice_powers = map(dice_power, minimum_list)
part2_sum = sum(dice_powers)
print(f"Challenge 2: {part2_sum}")
