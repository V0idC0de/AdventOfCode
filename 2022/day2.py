from typing import Tuple, List

with open("day2.txt") as f:
    lines = f.readlines()

rounds: List[Tuple] = [tuple(l.strip().split()) for l in lines]
rounds = [("ABC".index(p1), "XYZ".index(p2)) for p1, p2 in rounds]


def choice_score(p2: int) -> int:
    return [1, 2, 3][p2]


def win_score(p1: int, p2: int) -> int:
    # --> (p2 - p1) % 3
    # 0 = draw
    # 1 = win
    # 2 = loss
    return [3, 6, 0][(p2 - p1) % 3]


def result_to_choice(players: Tuple[int, int]) -> Tuple[int, int]:
    p1, p2 = players
    return p1, (p1 + (p2 - 1)) % 3


print(f"Part 1: {sum(choice_score(p2) + win_score(p1, p2) for p1, p2 in rounds)}")
print(f"Part 2: {sum(choice_score(p2) + win_score(p1, p2) for p1, p2 in map(result_to_choice, rounds))}")