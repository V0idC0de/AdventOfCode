# Advent of Code

Contains my solutions to "[Advent of Code](https://adventofcode.com/2023)" of 2023,
along with my inputs for all challenges.

## Requirements

Python 3.12+ (no additional packages required)

## Logbook

### Day 1

Approach was siple, get all numberic characters, pick the first and the last, then combine them to a number.

Part 2 was more tricky. Simply replacing number-terms (one, two, ...) wasn't sufficient, since terms like "eightwo"
could appear. When replacing number-terms in order ("two" before "eight"), "eightwo" becomes "eigh2".

To solve it, I declare all valid search terms (digits and digit-words) and found
the highest and lowest index for each, not replacing anything at all.
The occurrences with the lowest and highest digit respectively won and formed the final solution number.

### Day 2

Day 2 was really just a min()/max() game. Nothing special to note here.

### Day 3

Already afraid that part 2 could kill my approach from part 1 (foreshadowing lol), I picked an approach where I would
take the index range of every number and then check the surrounding fields for any special characters.
If at least one character was present, the number would be counted. Otherwise, it's ignored.

Part 2 forced me to not only detect whether a symbol was present, but also how many.
Since numbers that touch a "gear" could extend in any direction, also beyond the direct surrounding of a gear,
it was tricky at first, to find a simple solution.

I chose to once again get all fields that are occupied by digits belonging to a number.
Then I placed information about the full number on each grid-field a digit of this number was present.
This way, it would be very easy to check the close proximity of a "gear" for exactly two fields with numbers on them.
As a single field of the full number contains all information about it, I could easily get the full number by stumbling
upon a single field. In addition, I made each field of a number, reference the same object, so if multiple fields around
a "gear" contained a number object, I could easily tell whether they are two fields of the very same number,
using **Object Identity**.

Then just find the gears with exactly two numbers around them and calculate the solution value.

### [Days to be done ...]

Will comment on those, when I feel like it.

### Day 14

Simulating "tilting the platform" could be done by sorting a line consisting of "." and "O" characters.
However, since "#" character aren't supposed to move and block all following "rocks", I split the line at "#",
sorted each segment and then joined the segments together again separated by "#".
This worked quite well for part 1.

As usual, part 2 takes this and scales the problem, now requesting 4 * 1 Bn. "tilts".
Doing it normally takes an enormous amount of time, but since the function sorting the lines,
as well as the function for performing a full tilt are probably called with identical input many times,
I used `functools.cache()` to get their results quicker.
Doing this required using a `tuple[str]` as input, as opposed to `list[str]`, but increased performance to a point,
where part 2 would also finish in a few minutes.

> I noticed that the weights become cyclic rather quickly, so performing the full 10^9 iterations is not necessary.
> It's perfectly possible to detect the cycle, see how many steps are left to 10^9, and then use a modulo-calculation
> to see, where the 10^9-th iterations ends up in the cycle.
>
> Since the cycle length is unknown, I'd have to record the state after doing one cycle and check if it's a known state.
> In essence this is similar to **Day 8**, where instead of doing an exhaustive simulation,
> we detect the cycle and then predict where the last step ends up.

### Day 15

Implementing the hash functions was easy using `ord()` which returns the ASCII code for each character.
Adding `functools.cache()` to the hash-function increased performance slightly.

Part 2 was also simple, since Python has ordered `dict`s (normal `dict`s are ordered by default since Python 3.7),
hence being a perfect fit for the task of storing the lens' label along with it's **focal length**.
Replacing existing lenses for appending it to the box/`dict` is handled perfectly, by just writing to the `dict` -
not much of a difficulty here.

### Day 16

todo

### Day 17

Reading the task was already "**oof**". Clearly a path-finding/path-optimization, with restrictions on how the Graph
can be traversed. I skipped it at first, but then went back to it, as it nagged my mind, that I kinda knew the solution.

**Dijkstra** was an obvious contender for the algorithm, although I had to tweak a few things to make up for the rules
of this particular task. After refreshing my knowledge on how Dijkstra works exactly, I tweaked the following:

1. I don't need to list all of the nodes, since I'm just interested in the shortest path to one of them
2. I don't need to store the previous node for each connection, since I'm not looking for a path, but only for
   the minimum distance from start to finish. I was a little afraid that part 2 would require it, but adding it
   afterwards
   would be quite easy, so I skipped it for now - looking back, the right choice.
3. Last, but definitely not least: Since there are rules regarding the maximum (and in part 2 also minimum) steps to
   take in each direction, this effectively doubled the amount of nodes, since now the directions, one **must** take
   when leaving the node is relevant.

I chose an approach where the connected nodes of a given node `N` are defined as **all nodes, which are `i` steps away
from `N` in a direction of `d`. The direction of those nodes is the one, which `d` is not.**

- `i` is any amount that is allowed to move. **1-3** in part 1, **4-10** in part 2.
- `d` is an instruction, allowing 2 directions, either being `-` for horizontal movement (left/right) or
  `|` for vertical movement (up/down).

> Since the crucible cannot turn around entirely and we assume that `i` steps are taken and a 90° turn is done
> afterwards, it's sufficient to alternate the direction `d`, to indicate in which direction the crucible can move next.
> Both possible directions, resulting from `-` (left/right) or `|` (up/down) are explored.

For each node, we then just go ahead and see which nodes it can move to and how much heat-loss in incurred.
Then, we merge that into the heat-loss mapping, in case we found a better solution than the previously known one.

As soon as the target tile is part of the heat-loss mapping, we know that we've found a way.
In fact, we found the optimal way, since **Dijkstra always finds an optimal solution first**.

> The runtime is pretty long with around half a minute on my machine for the puzzle input.
> I couldn't come up with a smart improvement, if there is any - but couldn't be bothered to look one up either,
> since I'm a few days behind.