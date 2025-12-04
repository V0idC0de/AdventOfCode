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