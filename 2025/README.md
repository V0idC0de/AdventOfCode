# Advent of Code

Contains my solutions to "[Advent of Code](https://adventofcode.com/2025)" of 2025,
along with my inputs for all challenges.

## Requirements

Python 3.12+ and all packages listed in `requirements.txt`.

Use `pip install -r requirements.txt` to install them. Optionally do so in an virtual environment
by using `python -m venv .venv` and activating it afterwards with `source .venv/bin/activate` (Linux/Mac)
or `.venv\Scripts\activate` (Windows).

## Logbook

### Day 1

Intuitively this can be solved by just generation all positions the dial will end up in.
In Python, a neat solution for this is the `yield` statement, which allows to create a generator function.
This saves memory, as not all positions have to be stored at once - generally a good practice.

Then we just iterate through the results, given the puzzle input as instructions.
Each line in the puzzle input is converted into a positive or negative integer, depending on `L` or `R`.
This way, we can simply add the values to the current position, modulo the number of positions on the dial.

> [!NOTE]
> On this occasion, I learned that some languages like **Odin** feature two Modulo operators.
> The **Euclidean Modulo** always returns a positive result (**favorable in this task**),
> implementing the expected "wrap-around".
> However, there is another Modulo operator (remainder), which may also return negative numbers,
> if the number being divided is negative.

Now that we can go through each position in a very memory-efficient way, we can simply compose all
positions, which end up being `0` in a list and get its length - here we have the solution for part 1.

Part 2 is similar, but now we have to detect every single time a dial move touches `0`.
Starting positions are always positive. For the dial move there are two cases:

1. The move is positive. In that case, we can just add it to the current position to receive the `new_position`, then
    1. perform `new_position % dial_size` to get the wrapped-around new position
    2. perform an integer division of `(current_position + move) // dial_size` to get the number of times we touch `0`,
       which happens on every "wrap-around".
2. The move is negative. Here we can also just add the numbers to get the new position, then do the following
    1. perform `new_position % dial_size` to get the wrapped-around new position, which works properly,
       if **euclidean modulo** is used.
    2. calculate the number of times we touch `0` by performing the integer division
       of `abs(new_position) // dial_size`.

However, **case 2** has a nasty catch: We have to account for the case, when `0` is touched by decreasing the dial
and "underflowing" it below `0`, which is not accounted for by the integer division. **So if `new_position` is less
or equal to `0`, we have to add one more touch of `0` to the count.**

**This however has a second catch:** If the position already was exactly `0` before applying the move,
then we **must not** give this extra count, since the last move already did and we would double-count it.

Effectively, we give the extra count, if `old_position != 0 and new_position <= 0`, so the dial crossed `0`.
This took a few tries to figure out, but after this, I'm quite happy with the solution. Nice first puzzle.

### Day 2

This puzzle could be done via string-manipulation and string-slicing, but that seemed rather easy.
To tackle this as a kind of "performance challenge", I tried to do it with arithmetics only.

To make a number of length `n` repeat, you can utilize a multiplication. For example:

```plain
Repeat 80 twice (80 --> 8080):
80 * 1 = 80
80 * 100 = 8000
--> (80 * 100) + (80 * 1) = 8080

Repeat 750 three times (750 --> 750750750):
750 * 1 = 750
750 * 1000 = 750000
750 * 1000000 = 750000000
--> (750 * 1000000) + (750 * 1000) + (750 * 1) = 750750750
```

What sticks out here, is that a repeating number can be built by multiplying it by powers of 10 and summing the results.
Which powers to use depends on the numbers you're looking for. Let's use the trick in both parts and implement a
function
which checks, whether a number is made up of a repeated sequence of numbers.

> [!NOTE]
> A way to get the length of a number would be `len(str(n))`, however this converts the number to a string and
> turned out to basically double the execution time of the solution. Casting is expensive.
> Better use `math.log10(n)` to get its "magnitude", then apply `math.floor()` and add `1` to get the length of the
> number.

For part 1, we have to find numbers that repeat twice.
We can already declare all numbers with an odd length to be non-repeating, since their length cannot fit two equal
parts.

The idea is the following:

1. grab the first half of the number arithmetically (`258258` --> `258`)
2. then repeat it using a multiplication (more on that in a second)
3. check whether the result equals the original number

For part 1, we only have to do this for one repetition, so our multiplier is `1 + 10^x`,
where `x` is exactly half the length of the number.
For example, for a 6-digit number of `258258`, the multiplier is `1 + 10^3 = 1001`,
making the check look like `258 * 1001 == 258258`. Here, we compare the result to the original number.
If it matches, the repeating number is found and we return `True`.

For part 2, we have to account for repetitions of arbitrary length (obviously up to half the length of the number,
to fit at least one repetition).
Here, we basically add a loop around the logic from part 1, checking for all possible repetition lengths.

So we start by checking for a repetition length of `1` (e.g. `7777`), then `2` (e.g. `1212`),
then `3` (e.g. `258258`), and so on, up to half the length of the number.
If any of those checks return `True`, we have found a repeating number and can return `True`, otherwise `False`.

Instead of just adding `1` and `10^x` for the multiplier, we have to have one element for each repetition.
To construct our multiplier, we step from `0` up to the length of the original number minus
the length of the repeating part - this ensures we end up in the same length/magnitude as the original number.

So for `258258258258` we construct the multiplier for a repetition length of `3` like this:

```plain
length of original number: 12
length of repeating part: 3
number of repetitions: 12 / 3 = 4

10^0  +  10^3  +  10^6  +  10^9 
=  1 + 1000 + 1000000 + 1000000000
= 1.001.001.001
```

And to verify whether `258258258258` is made up of `258` repeated 4 times, we do `258 * 1.001.001.001` and
check whether it equals the original number.

To get this repeated number, we can perform an integer division of the original number by
`10^(length of original number - length of repeating part)`. This "cuts off" the last parts of the number,
as it slips behind the decimal point and is discarded by the integer division.

This way, we can solve both parts of day 2 with pure arithmetics, without any string manipulation at all.

#### Performance notes

Performance-wise this solution was a little lackluster. Initially, execution took around 6-7 seconds total
for both parts. However, I determined that `str(number)` to determine the length is very expensive.
Replacing it with `math.log10()` reduced execution time to around 3 seconds - **a speed-up of 100%!**

Another considerable improvement was using `@numba.njit` as annotation for the function checking for repetitions.
Since we're using almost pure arithmetics here, Numba can compile the function to machine code quite well.
This speeds up execution from ~2.6 seconds to ~1.8 seconds on my machine, yielding another **100% speed-up!**

Generally, Python is not a performance powerhouse, but these improvements were quite cheap, especially adding Numba.
Considering the effort was basically `pip install numba`, the speed-up is quite worth it. Definitely a recommendation.

Another idea was - as usual - to throw multiprocessing at this, since it's a CPU-bound task.
However, since the overhead of starting multiple processes and distributing the workload is quite high,
compared to the actual runtime, it turned out to actually **increase** execution time.
For bigger inputs, it would be worth it, of course.

### Day 3

This task was surprisingly fast to implement. Finding the highest two digit number basically boils down to applying
`max()`` twice. There are two catches:

1. Since we always want the higher digit in the higher position, we can only find the next digit AFTER the position
   of the previous one. So `max()` is only applied to the trailing list elements after the previously found digit.
2. This also implies a restriction. We have to exclude a few elements at the end of the list from being considered
   in `max()`, since we need enough elements to fill the rest of the number. If the amount of batteries we want to
   activate is `3`, then the first iteration has to exclude the last 2 elements, since we need at least two more digits
   after finding the first one.

To put it more generally, if we want to activate `n` batteries and the bank has `m` batteries total,
then the first iteration of `max()` has to only consider the first `m - (n - 1)` elements, as to leave at least
one for each following iteration.

Also, to calculate the final joltage with arithmetics only (instead of just concatenating the digit characters and
casting them to an integer), we can use powers of ten, similar to [Day 2](#day-2).

If we enable `n` batteries, the `i`-th battery's joltage contributes with a higher significance to the total.
That significance is simply a multiplier of `10^x`, where `x` is `n - i`, so if we enable `4` batteries,
our number would look like `9731`, so the `1`st iteration contributes `9 * 10^(4-1) = 9 * 10^3 = 9000`,
the seccond `7 * 10^(4-2) = 7 * 10^2 = 700`, and so on.

> [!NOTE]
> The usual suspect "off-by-one"-error is around again - do mind a shift of `-1` in the exponent, if you count your
> iterations from `0`!

When implementing all of this, I pre-emptively solved part 2 as well, since it just asked for another constant
amount of batteries to be activated, allowing the `max()`-search to just be run `n` times.

The Syntactic Sugar of this solution is a recursive invocation, since finding the best battery to activate is always
the same problem and finding the battery after this one is just repeating this process with the end-slice of the
input list and a decremented `n`, so the function knows how many batteries are still to be activated.

Termination condition is just `batteries_to_be_enabled == 0`, since there is nothing to activate anymore, returning `0`.
Adding all results together yields the final joltage.

### Day 4

For this day, there was a kinda obvious solution, similar to an implementation of a previous year.
This would have been to just build a 2D-Array, iterate through each element, find its neighbors and increment by one and
then check for field with a count less than 4.

However, I wanted to build something different. An idea was to try this as a 1-dimensional array,
where the sections for each row are calculated arithmetically. Also, I wanted to avoid maintaining a second grid
tracking the counts for each neighbor.

This sparked the approach in the implementation, which revolves around a single list of booleans,
which is the puzzle input, joined into a single line, keeping track of the `row_length` and `total_length`, of course.
Having this, I took all indices that are `True`, thus are "paper rolls". Based on that index, you can easily calculate
neighbor-indices, by adding for subtracting `1` (right/left) and/or `row_length` (down/up).

I would just do this for all paper rolls and let them announce their neighbors.
Then I'd utilize `itertools.Counter` to count the occurrences of each neighbor, thus "how often was each index
announced to be a neighbor of some paper roll?".

Filtering these indices for the ones that occur less than `4` times and are actually paper rolls
(because empty fields were also announced as neighbors of a roll) gives me all paper rolls with less than 4 neighbors.

However, there was a hard-to-find bug in this approach: Paper rolls with ß neighbors were not counted at all,
but are valid answers. So I fixed it by going through the original list of paper rolls and checking each in the
`Counter` **assuming `0` neighbors, if not found in the `Counter`**. This yielded the correct result and identified
the indices of the "available paper rolls".

The second part was an iteration of the first: Now, we just set the returned "available paper rolls" to `False`
in the inventory list of booleans, emulating their "removal" from the fields.
We now perform the algorithm of part 1 again, finding the next set of available paper rolls.
If this algorithm ever returns `0` available rolls, we converged to a result, where we can no longer remove anything.

The sum of all returned "available paper rolls" over all iterations is the answer to part 2.

> [!NOTE]
> This approach is not the most efficient one, since we re-calculate the entire neighbor counts for each iteration.
> I just followed through on this approach, since it was an interesting exercise and applied a different concept.

#### Alterantive solution for part 2

One could also choose a more efficient approach of "removing a paper roll" by maintaining a grid,
tracking "amount of neighbors". Then, we do the following:

1. Find all indices of paper rolls, available for removal (less than 4 neighbors)
2. For each index to be removed, do the following
   1. Set its field to `False` to indicate that there is no longer a roll
   2. Subtract `1` from each of its neighbors in the "neighbor count" grid
   3. On subtracting from a neighbor count field, check if the count is now less than `4`
   4. If 2.3. is `True`, remove that field by doing all steps of step 2 recursively for that field, then continue here

Once this recursive algorithm finishes, all possible removals are done and we only evaluate fields, whose count changes.
Since a field has to change its count in order to become available for removal, it is sufficient to check changing
fields.

Complexity for this approach is minimized for the repeated checking of all fields, performing only necessary
comparisons, instead of re-evaluating the entire grid each iteration and converging to a result.

### Day 5

This was also pretty straightforward and can easily be done with Python's `range()` function/objects.
`x in range(1, 10)` can easily check whether `x` is in the range from `1` to `9` (inclusive of `1`, exclusive of `10`).

An alternative is a condition like `1 <= x && x <= 9`, given that `x` is the Ingredient ID and `1`/`9` are range bounds.

Python's `map()` and Generator expressions make it easy to iterate through the ingredients and be as memory-efficient
as possible, since these Iteration generally do lazy-evaluation.

Part 2 was surprisingly tricky, as the sheer calculation of range-size ignored overlaps, counting IDs mutliple times.
However, just using `itertools.chain.from_iterable(fresh_ranges)` solves the issue but take **VERY** long,
since the result is so big.

An alternative solution was to use a function (implemented in Python as a Generator with `yield`) to "compact" ranges.
By sorting the ranges and then going through each of them, we can just combine by two ranges by doing the following:

1. `r1` and `r2` are combined
2. If `r2.start` is less or equal to `r1.end + 1`, then the ranges overlap or touch (`range.stop` is exclusive,
   so `r2.start > r1.stop + 1` is a distance of at least one ID).
   - In this case, we cannot combine the ranges, so we yield (or store in other language) the currently stored `start`
     and `stop` values as a `range` object
3. If `r2.start` is within `r1` or `r1.end == r2.start` we have "touching" or overlapping ranges.

- In this case, set the `r1.end` to `max(r1.end, r2.end)`, as `r2` might end before `r1`.

This causes ranges to be expanded as much as possible and stored once the next range is separated.
**Sorting is essential** since it guarantees that after a `range.start` was deemed "separated",
no subsequent range can start earlier than that and potentially overlap with the current one.

> [!NOTE]
> A neat detail, which is also why I'm working with `range` object instead of tuples, is that `len()` is supported
> on `range` objects, allowing very quick calculation of the size of a range with arithmetics in a very
> well readable and "pythonic" way.

# Day 6

This challenge was surprisingly difficult, since I got entangled in nested data structures.

Part 1 was straightforward. `str.split()` lines and remove empty entries to account for multiple spaces.
Then convert the number to integers, transpose the resulting lists, so we have all first elements together,
which represents one colum of input, which is one calculation.

To add things together, I took the opportunity to use one of my favorite functions: `functools.reduce()`.
Kinda "overkill", but I suspected that part 2 changes the operators and this approach would make that easy and elegant.

Part 2 hit different, though. First, I entirely misread the task and thought the numbers should be read backwards. (lol)
After realizing what should really be done, I got really entangled in nested lists and data structures.
Breaking things down into smaller parts and doing one thing at a time helped a lot.

Since now spaces and position of single numbers in a column was crucial, I could no longer naively `str.split()`.
Realizing that operators indicate the beginning of a number column allowed me to quickly build a list of start-indices
and that columns width/`len()`.

This way, I could correctly slice each line into pieces, keeping spaces intact.
The approach was to basically build a matrix of characters representing a column and transposing it to get the numbers
read vertically.

Two caveats I ran into and had to work around:

1. The **operator-line** is shorter than the **number-lines**, since the last operator is the last character,
   but all numbers greater than 9 need more than one character. So the last length has to be the maximum length of all
   lines, not just the **operator-line**.

2. Spaces generally must be considered as zeroes, since `420`, `69`, `337` has to result in `403` in the first column.
   However, `42 `, `123`, `69 ` (do note the spaces) has to result in `3` in the last column, not `30`, as a plain
   `replace(" ", "0")` would yield. So composed number-strings have to be `strip()`-ed before converting to integers.

Ultimately, this challenge was a very neat AoC challenge, since the task was visually easy to understand
(minus the treatment of spaces and alignment of numbers, but that might as well just be me 🤡), but a little tricky
to implement and find the right structures to represent.

# Day 7

For this challenge, there is not much finesse involves, this time.

The puzzle can be solved by "applying" each line to set of indices (X-coordinate of the tachyon beams), that are
occupied by a beam. If one beam index matches a splitter index, remove it and add the two adjacent indices,
increasing a "split-counter" in the process. Puzzle solved.

Part 2 reminded me of a puzzle in 2023 and prompted me to apply, what I learned there years ago.
Here, we can treat the beam position as a kind of "state machine", counting the number of timelines in a given
state (= X-coordinate).

We start with a dictionary, tracking indices mapped to number of timelines to reach that state.
This `dict` starts with the starting position of `S` and setting that index to `1`, so `{70: 1}` for me.

Then we go through each line of input, checking for splitters at indices which are present in our `dict`.
If a splitter is found, copy the value of that index to the two adjacent indices and remove the original index,
since the beam is stopped by the splitter.

`sum()` all values after applying all input lines and there is the result.

# Day 8

This puzzle was interesting, as it consisted of two stages. First, quickly calculate the order of
Junction Boxes to connect. Then calculate the circuits.

Part 1 was solved by having a `dict`, mapping each Box to the circuit it belong to. Circuits are represented
by `set`s of Boxes. Initially, all Junction Boxes are in their own circuit.

Then, for each connection, we check whether the two Boxes are already in the same circuit, so `{ b : {b} }`.
To make a connection, we simply construct the **set union** of both circuits.
Then, for each Box that is contained in the new circuit, we set their value to our new circuit.

In Python, variable are all passed by reference, so in the end, there are as many sets as there are circuits.
However, since circuits are necessarily partitions of the set of all Boxes, it could also be calculated that way.

Part 2 asked to create connections, until there is only one big circuit. The same approach applies here,
since we can just add connections with the same logic as in part 1, until the length of our **set-union** is equal
to the number of Boxes.

# Day 9

The first REALLY hard puzzle, at least for me. Similar to a puzzle in 2023, it required areas and borders to be
calculated, based on whether they are contained in each other.

Part 1 was very straightforward and made great use of Python's `itertools` library. Try all combinations,
find the one with the biggest area - done.

Part 2 was very tricky. I actually didn't find an elegant solution to begin with.
Not wanting to resort to brute-force or enumerating all valid tiles (since it scaled horribly),
I considered approaches, which make use of the vectors connecting tiles, etc.

However, after hours of pondering ideas and always running into dead-ends, I skipped this part,
since I didn't see any option to come up with a solution myself, so that star is not deserved.

> Some posts on [/r/adventofcode](https://www.reddit.com/r/adventofcode/) mentioned ray-casting, which I also
> considered,
> but couldn't entirely think through. One particularily clever individual just used `shapely` to draw the shapes and
> let the library calculate, whether the square is contained in the bigger shape. Just "lol".

# Day 10

Day 10 was very two-sided. Part 1 rewarded the solver for careful reading of the task and realizing a few things about
logic and the input. Part 2 required a specific application of linear algebra to solve the problem reliably.

In part 1 the following came to mind:

- the lights are toggled on and off, which effectively is an XOR operation
- toggling a light twice results in no change at all, so 2 presses = 0 presses
- this implies, that 3 presses = 1 presses, which means that the question becomes
  **whether** a button is pressed, not **how often** it is pressed
- XOR is commutative, so the order of presses does not matter

I represented the lights in binary as a bitmask, so `.#.#` --> `0101`.
Then, `itertools` could easily generate all combinations of button presses in ascending length,
so first all single presses, then all combinations of two presses, etc.

This Breadth-First Search guarantees that the first time we reach the target state, we also found the minimum.
To check whether a solution is found, we check whether the XOR of the lights desired state XOR all button presses
yields `0`, so all lights are off. Of course, we could also XOR `0` with all button presses, since XOR is commutative.

The bitmasks for buttons can easily be built by bit-shifting `1` to the left by the button index.

Part 2 was a lot more tricky and couldn't be solved in a short time by brute forcing,
since the amount of button presses (which was at least the maximum in the list of required Joltages)
yielded so many combinations, that brute forcing was not feasible.

After some tinkering, I realized that the Joltages can be represented as a vector and the effects of each button
can construct a matrix. Therefore, I was sure the approach was to solve a system of linear equations.

However, I struggled a lot with resolving the matrix and interpreting the results I was getting.
Checking [/r/adventofcode](https://www.reddit.com/r/adventofcode/) posts after I gave up at 3:00 AM,
posts confirmed that I was on the right track. I didn't feel like getting into an entirely new library to
solve the matrix and read up on interpeting Linear Algebra results, so I gave up on this part.

> The numbers on the Stats-page confirmed that this was a rather hard puzzle with less than half of all solvers
> being able to solve part 2. For now, I'm satisfied with finding the right track, even though I couldn't implement it.

# Day 11

Refreshingly simple compared to day 10.

Part 1 could be solved recursively by building a function, which finds the number of possible paths,
by returning `1` if the destination is reached and otherwise summing the number of paths from each possible next step,
according the static available connection map given in the puzzle input.

Utilizing `@functools.cached` this was also quite fast and very few lines of code.
Interestingly, the sequence of steps didn't matter, just the number of steps.
This made use of the fact, that **there are no cyclic paths**, which is implied by the question asking for the amount
of possible paths, which becomes `∞` if cycles were possible.

Part 2 could also be solved by using a simple calculation and my approach from part 1.
Since now, `fft` and `dac` need to be visited in arbitrary order, the following is possible:

- `start` --> `fft` --> `dac` --> `end`
- `start` --> `dac` --> `fft` --> `end`

Using `start`, `fft`, `dac`, and `end` as start-points and end-points for the path-search already implemented
in part 1, this yields 6 sections of the path.

Multiplying the number of possible paths for each segment of a possible sequence yields the possible paths
to achieve that sequence. Since there are only two sequences (see bullet points above), summing both results
yields the answer to the puzzle, without any extra complexity.

> The only caveat was, that `end`-node had no paths going forward and is not the destination in part 2,
> which yielded a few `KeyError`s when looking up the next possible nodes.
> Simply returning `0` possible paths in this case was sufficient, to indicate that this path is a dead-end.
