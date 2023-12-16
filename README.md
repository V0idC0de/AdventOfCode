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