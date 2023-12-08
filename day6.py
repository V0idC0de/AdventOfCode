import operator
from collections.abc import Generator
from functools import reduce
from typing import NamedTuple

Race = NamedTuple("Race", time=int, distance=int)
Settings = NamedTuple("Settings", button_duration=int, distance=int)

races = [
    Race(47, 282),
    Race(70, 1079),
    Race(75, 1147),
    Race(66, 1062),
]


def calc_distances(available_time: int, required_distance: int) -> Generator[Settings]:
    settings = (Settings(i, i * (available_time - i)) for i in range(1, available_time))
    return (s for s in settings if s.distance > required_distance)


# Part 1
race_solutions = (list(calc_distances(r.time, r.distance)) for r in races)
variant_product = reduce(operator.mul, map(len, race_solutions))
print(f"Challenge 1: {variant_product}")

# Part 2
race = Race(47707566, 282107911471062)
win_conditions = list(calc_distances(race.time, race.distance))
print(f"Challenge 2: {len(win_conditions)}")
