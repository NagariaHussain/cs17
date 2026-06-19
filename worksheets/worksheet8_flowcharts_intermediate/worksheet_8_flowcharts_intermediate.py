"""Intermediate Flowcharts Worksheet — loops that carry more state.

A follow-on to Worksheet 7 (Simple Loops). Worksheet 7 covered the basic loop
shapes, each with a single counter. The loops here are a step up: they keep TWO
running values at once (Fibonacci, Euclid's GCD), pull a number apart digit by
digit with remainder (%) and whole-number division (//), or run a decision
*inside* the loop (Collatz). The same two problem types are mixed:

  TRACE(algo, {...})  given the flowchart + inputs -> fill the trace table
  DRAW(algo, ...)     given a plain-English statement -> draw the flowchart

As in the other flowchart worksheets, each algorithm is authored once and the
flowchart, pseudocode, and trace table are all derived from the same source.
"""

from gens.flowgen import Algorithm, read, assign, out, If, While, TRACE, DRAW

TITLE = "Worksheet 8: Flowcharts (Intermediate)"

# A reminder shown on the first problem that uses % and //, reused below.
DIV_NOTE = ("Reminder: n % 10 is the remainder when n is divided by 10 (the "
            "last digit of n), and n // 10 is n divided by 10 with the remainder "
            "thrown away (which drops the last digit) — so 4072 % 10 is 2 and "
            "4072 // 10 is 407.")

# A reminder shown on the first problems that index a list, reused below.
INDEX_NOTE = ("Reminder: the items of a list have positions counted from 0, so "
              "the list [4, 7, 2, 9, 5] has 5 items in positions 0 to 4 — "
              "position 0 holds 4, position 1 holds 7, and so on. arr[i] means "
              "the item at position i, so arr[0] is the first item.")

# --- list traversal: walk a list one item at a time, from position 0 up --------

# T1. the simplest traversal: add up every number in the list
sum_list = Algorithm("Sum of the numbers in a list", [
    assign("sum", "0"),
    assign("i", "0"),
    While("i < 5", [
        assign("sum", "sum + arr[i]"),
        assign("i", "i + 1"),
    ]),
    out("sum"),
])

# T2. traversal that keeps a "best so far": the largest number in the list
largest = Algorithm("Largest number in a list", [
    assign("max", "arr[0]"),
    assign("i", "1"),
    While("i < 5", [
        If("arr[i] > max",
           [assign("max", "arr[i]")]),
        assign("i", "i + 1"),
    ]),
    out("max"),
])

# T3 (draw). traversal that prints as it goes: each number, doubled
double_each = Algorithm("Print each number in the list, doubled", [
    assign("i", "0"),
    While("i < 5", [
        out("arr[i] * 2"),
        assign("i", "i + 1"),
    ]),
])

# 1. two running values: print the first n Fibonacci numbers (0,1,1,2,3,5,8,...)
# Keep the last two numbers in a and b; compute `next` BEFORE overwriting a.
fibonacci = Algorithm("First n Fibonacci numbers", [
    read("n"),
    assign("a", "0"),
    assign("b", "1"),
    assign("i", "1"),
    While("i <= n", [
        out("a"),
        assign("next", "a + b"),
        assign("a", "b"),
        assign("b", "next"),
        assign("i", "i + 1"),
    ]),
])

# 2. take a number apart digit by digit and add the digits up
sum_of_digits = Algorithm("Sum of the digits of n", [
    read("n"),
    assign("sum", "0"),
    While("n > 0", [
        assign("sum", "sum + n % 10"),
        assign("n", "n // 10"),
    ]),
    out("sum"),
])

# 3. the same digit-peeling loop, but just counting how many digits there are
count_digits = Algorithm("Number of digits in n", [
    read("n"),
    assign("count", "0"),
    While("n > 0", [
        assign("count", "count + 1"),
        assign("n", "n // 10"),
    ]),
    out("count"),
])

# 4. Euclid's algorithm — two running values, swapped each step via a remainder
gcd = Algorithm("Greatest common divisor of a and b", [
    read("a"),
    read("b"),
    While("b != 0", [
        assign("r", "a % b"),
        assign("a", "b"),
        assign("b", "r"),
    ]),
    out("a"),
])

# 5. a decision INSIDE the loop: the Collatz / hailstone sequence — count the
# steps to reach 1 (even -> halve, odd -> triple-plus-one)
collatz = Algorithm("Steps for n to reach 1 (Collatz)", [
    read("n"),
    assign("steps", "0"),
    While("n != 1", [
        If("n % 2 == 0",
           [assign("n", "n // 2")],
           [assign("n", "3 * n + 1")]),
        assign("steps", "steps + 1"),
    ]),
    out("steps"),
])

# 6. build a NEW number a digit at a time: reverse the digits of n
reverse_number = Algorithm("Reverse the digits of n", [
    read("n"),
    assign("rev", "0"),
    While("n > 0", [
        assign("rev", "rev * 10 + n % 10"),
        assign("n", "n // 10"),
    ]),
    out("rev"),
])

# 7. two pointers narrowing a window: binary search a SORTED list for a target.
# `arr` is a given array (a tuple input) the algorithm indexes but never reads,
# so it never becomes a trace-table column. The list has 10 items, positions
# 0..9, so the search starts with low = 0 and high = 9. found stays -1 until the
# target turns up, and the loop stops as soon as it does.
binary_search = Algorithm("Binary search for target in a sorted list", [
    read("target"),
    assign("low", "0"),
    assign("high", "9"),
    assign("found", "-1"),
    While("low <= high and found == -1", [
        assign("mid", "(low + high) // 2"),
        If("arr[mid] == target",
           [assign("found", "mid")],
           [If("arr[mid] < target",
               [assign("low", "mid + 1")],
               [assign("high", "mid - 1")])]),
    ]),
    out("found"),
])

PROBLEMS = [
    TRACE(sum_list, {"arr": (4, 7, 2, 9, 5)},
          description="This program adds up all the numbers in a list. It keeps a "
                      "running total in sum and a position marker i, and walks "
                      "through the list one item at a time — from position 0 to the "
                      "last — adding each item to the total as it goes.",
          note=INDEX_NOTE),

    TRACE(largest, {"arr": (3, 9, 2, 12, 7)},
          description="This program finds the largest number in a list. It begins "
                      "by assuming the first item (position 0) is the biggest, then "
                      "walks through the rest of the list: whenever it meets an item "
                      "bigger than the best seen so far, it remembers that one "
                      "instead. max holds the largest value found so far.",
          note=INDEX_NOTE),

    DRAW(double_each,
         description="Go through a list of numbers from start to finish and, for "
                     "each one, print that number multiplied by 2 — for example, "
                     "for the list [2, 5, 0, 1, 4] the program prints 4, 10, 0, 2, "
                     "8.",
         predict=[{"arr": (3, 8, 1, 6, 4)}, {"arr": (10, 0, 5, 2, 7)}]),

    TRACE(fibonacci, {"n": 7},
          description="The Fibonacci sequence starts 0, 1 and then every number "
                      "after that is the sum of the two before it (0+1=1, 1+1=2, "
                      "1+2=3, and so on). This program prints the first n numbers "
                      "of the sequence. It keeps the last two numbers in a and b: "
                      "each time round the loop it prints a, works out the next "
                      "number (a + b) before changing anything, then slides the "
                      "pair along so a and b become the next two numbers."),

    TRACE(sum_of_digits, {"n": 4072},
          description="This program reads a whole number and adds up its digits. "
                      "It peels off the last digit each time (using the remainder "
                      "after dividing by 10), adds it to a running total, then "
                      "drops that digit and repeats until nothing is left.",
          note=DIV_NOTE),

    DRAW(count_digits,
         description="Ask the user for a whole number n and print how many digits "
                     "it has — for example 4072 has 4 digits and 9 has 1 digit. "
                     "(Hint: you can drop the last digit of a number by doing "
                     "n // 10, i.e. dividing by 10 and throwing away the "
                     "remainder. Keep doing that, counting as you go, until the "
                     "number reaches 0.)",
         predict=[{"n": 4072}, {"n": 538}, {"n": 9}]),

    TRACE(gcd, {"a": 48, "b": 36},
          description="This is Euclid's method for the greatest common divisor "
                      "(the largest number that divides both a and b exactly). "
                      "Each step replaces the pair (a, b) with (b, remainder of a "
                      "divided by b); when the remainder reaches 0, the answer is "
                      "the value left in a.",
          note="Reminder: a % b is the remainder when a is divided by b "
               "(for example 48 % 36 is 12, and 36 % 12 is 0)."),

    TRACE(collatz, {"n": 6},
          description="Start from a whole number n and repeat one rule until you "
                      "reach 1: if n is even, halve it; if n is odd, replace it "
                      "with 3 × n + 1. This program counts how many steps that "
                      "takes. (No one has ever found a starting number that fails "
                      "to reach 1 — but no one has proved it always does, either!)",
          note="Reminder: n % 2 is the remainder when n is divided by 2, so "
               "n % 2 is 0 exactly when n is even; n // 2 is n halved with any "
               "remainder dropped."),

    DRAW(reverse_number,
         description="Ask the user for a whole number n and print the number you "
                     "get by reversing its digits — so 825 becomes 528 and 1900 "
                     "becomes 91 (leading zeros just disappear). (Hint: peel off "
                     "the last digit of n with n % 10, and grow a result by doing "
                     "rev = rev × 10 + that digit each time, while dropping the "
                     "digit from n with n // 10.)",
         predict=[{"n": 825}, {"n": 1900}, {"n": 7}]),

    TRACE(binary_search,
          {"target": 23, "arr": (2, 5, 8, 12, 16, 23, 38, 56, 72, 91)},
          description="Binary search finds where a target value sits in a sorted "
                      "list without checking every item. It tracks a window with "
                      "two markers, low and high (the positions still worth "
                      "searching, numbered from 0). Each step looks at the middle "
                      "position mid: if that item is the target we are done; if it "
                      "is too small the target must be to the right, so move low "
                      "up; if it is too big, move high down. found holds the "
                      "position of the target, or stays -1 until it is located.",
          note="Reminder: arr[mid] means the item at position mid of the list "
               "(positions start at 0, so arr[0] is 2); (low + high) // 2 is the "
               "middle position, dividing by 2 and dropping any remainder; and "
               "the loop keeps going while low <= high and found is still -1."),
]
