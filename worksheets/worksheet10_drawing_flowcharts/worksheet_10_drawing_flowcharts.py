"""Drawing-Flowcharts Worksheet — practice DRAWING, not tracing.

The earlier flowchart sheets (2, 7, 8) asked students mostly to *trace* a given
flowchart and fill a trace table. Students are now comfortable tracing but
struggle to *draw* a flowchart of their own. This sheet is therefore DRAW-only:
every problem is a plain-English statement, and the student draws the flowchart.

It ramps deliberately:

  Part A  straight-line (sequence)   — read, calculate, print: get the shapes right
  Part B  one decision               — a single if / else (one diamond)
  Part C  two decisions              — nested or combined conditions
  Part D  simple loops               — a while-loop, ending with a loop + decision

Modulo (%) and whole-number division (//) are mixed in throughout, since the
class already knows them. Each algorithm is authored once; the answer key's
flowchart, pseudocode, and the "predict the output" table are all derived from
that single source, so they can never disagree.

Most problems include a predict-before-you-draw step: the student first works
out by hand what the program should print for a few inputs, then — after drawing
— traces their own flowchart on those same inputs and checks it agrees. Hints
are given only where a mechanic (% , // , or how to grow a loop) is the point.
"""

from gens.flowgen import Algorithm, read, assign, out, If, While, DRAW

TITLE = "Worksheet 10: Drawing Flowcharts"

# ---- Part A: straight-line algorithms (sequence only, no decisions) ----------

# A1. two reads, two calculations, two prints — pure top-to-bottom sequence.
rectangle = Algorithm("Area and perimeter of a rectangle", [
    read("length"),
    read("width"),
    out("length * width"),
    out("2 * (length + width)"),
])

# A2. a sequence that uses // and % to split one number into two.
seconds = Algorithm("Minutes and seconds", [
    read("total"),
    assign("mins", "total // 60"),
    assign("secs", "total % 60"),
    out("mins"),
    out("secs"),
])

# ---- Part B: one decision (a single diamond, then merge) ---------------------

# B1. the classic single decision, driven by a remainder.
even_odd = Algorithm("Even or odd", [
    read("n"),
    If("n % 2 == 0", [out('"Even"')], [out('"Odd"')]),
])

# B2. one decision over a threshold.
pass_fail = Algorithm("Pass or fail", [
    read("marks"),
    If("marks >= 50", [out('"Pass"')], [out('"Fail"')]),
])

# B3. one decision comparing two inputs.
larger = Algorithm("Larger of two numbers", [
    read("a"),
    read("b"),
    If("a >= b", [out("a")], [out("b")]),
])

# B4. one decision again from a remainder — but the "yes" branch does more.
change = Algorithm("Can you buy it?", [
    read("price"),
    read("cash"),
    If("cash >= price",
       [out('"You can buy it"'), out("cash - price")],
       [out('"Not enough money"')]),
])

# ---- Part C: two decisions (nested, or two conditions combined) --------------

# C1. ONE diamond, but the condition combines two tests with "or".
divisible = Algorithm("Divisible by 3 or 5", [
    read("n"),
    If("n % 3 == 0 or n % 5 == 0",
       [out('"Divisible"')],
       [out('"Not divisible"')]),
])

# C2. a decision INSIDE the "no" branch of another — the grade ladder.
grade = Algorithm("Letter grade", [
    read("marks"),
    If("marks >= 80",
       [out('"A"')],
       [If("marks >= 50", [out('"B"')], [out('"C"')])]),
])

# C3. two nested decisions to pick the biggest of three.
largest = Algorithm("Largest of three numbers", [
    read("a"),
    read("b"),
    read("c"),
    If("a >= b and a >= c",
       [out("a")],
       [If("b >= c", [out("b")], [out("c")])]),
])

# C4. a three-way decision (>, <, equal) — Part C's capstone.
profit_loss = Algorithm("Profit, loss, or break-even", [
    read("cp"),
    read("sp"),
    If("sp > cp",
       [out('"Profit"'), out("sp - cp")],
       [If("sp < cp",
           [out('"Loss"'), out("cp - sp")],
           [out('"No profit, no loss"')])]),
])

# ---- Part D: simple loops (a while-loop with a counter) ----------------------

# D1. the simplest counting loop: print 1, 2, 3, ... up to n.
count_up = Algorithm("Print 1 to n", [
    read("n"),
    assign("i", "1"),
    While("i <= n", [
        out("i"),
        assign("i", "i + 1"),
    ]),
])

# D2. a counting loop that prints a calculation each time round.
times_table = Algorithm("Multiplication table of n", [
    read("n"),
    assign("i", "1"),
    While("i <= 10", [
        out("n * i"),
        assign("i", "i + 1"),
    ]),
])

# D3. a loop that builds up a running total (an accumulator).
sum_1_to_n = Algorithm("Sum of 1 to n", [
    read("n"),
    assign("sum", "0"),
    assign("i", "1"),
    While("i <= n", [
        assign("sum", "sum + i"),
        assign("i", "i + 1"),
    ]),
    out("sum"),
])

# D4. a loop whose counter is the NUMBER, shrunk with // until it runs out.
count_digits = Algorithm("Number of digits in n", [
    read("n"),
    assign("count", "0"),
    While("n > 0", [
        assign("count", "count + 1"),
        assign("n", "n // 10"),
    ]),
    out("count"),
])

# D5. capstone: a decision INSIDE a loop — print only the even numbers up to n.
print_evens = Algorithm("Even numbers up to n", [
    read("n"),
    assign("i", "1"),
    While("i <= n", [
        If("i % 2 == 0", [out("i")]),
        assign("i", "i + 1"),
    ]),
])

PROBLEMS = [
    # ---- Part A: sequence ----------------------------------------------------
    DRAW(rectangle,
         description="Ask the user for the length and width of a rectangle, then "
                     "print its area and its perimeter."),

    DRAW(seconds,
         description="Ask the user for a number of seconds and print how many "
                     "whole minutes it is, and how many seconds are left over.",
         predict=[{"total": 200}, {"total": 95}, {"total": 60}]),

    # ---- Part B: one decision ------------------------------------------------
    DRAW(even_odd,
         description="Ask the user for a number and print “Even” if it is even, "
                     "and “Odd” if it is not.",
         predict=[{"n": 7}, {"n": 10}, {"n": 0}]),

    DRAW(pass_fail,
         description="Ask the user for a student’s marks. Print “Pass” if the "
                     "marks are 50 or more, and “Fail” otherwise.",
         predict=[{"marks": 72}, {"marks": 50}, {"marks": 38}]),

    DRAW(larger,
         description="Ask the user for two numbers and print the larger of the "
                     "two.",
         predict=[{"a": 8, "b": 3}, {"a": 4, "b": 9}, {"a": 6, "b": 6}]),

    DRAW(change,
         description="Ask the user for the price of an item and how much cash they "
                     "have. If the cash is enough, print “You can buy it” and the "
                     "change they would get back. Otherwise, print “Not enough "
                     "money”.",
         predict=[{"price": 50, "cash": 80}, {"price": 50, "cash": 50},
                  {"price": 50, "cash": 20}]),

    # ---- Part C: two decisions -----------------------------------------------
    DRAW(divisible,
         description="Ask the user for a number. Print “Divisible” if it divides "
                     "exactly by 3 or by 5, and “Not divisible” otherwise.",
         predict=[{"n": 9}, {"n": 20}, {"n": 7}]),

    DRAW(grade,
         description="Ask the user for a student’s marks and print a letter grade: "
                     "“A” for 80 or more, “B” for 50 to 79, and “C” for below 50.",
         predict=[{"marks": 91}, {"marks": 64}, {"marks": 42}]),

    DRAW(largest,
         description="Ask the user for three numbers and print the largest of the "
                     "three.",
         predict=[{"a": 4, "b": 9, "c": 2}, {"a": 7, "b": 1, "c": 5},
                  {"a": 3, "b": 3, "c": 8}]),

    DRAW(profit_loss,
         description="A shopkeeper enters the cost price and the selling price of "
                     "an item. Print “Profit” and the profit if it sold for more "
                     "than it cost; print “Loss” and the loss if it sold for less; "
                     "and print “No profit, no loss” if the two prices are equal.",
         predict=[{"cp": 100, "sp": 130}, {"cp": 100, "sp": 80},
                  {"cp": 100, "sp": 100}]),

    # ---- Part D: simple loops ------------------------------------------------
    DRAW(count_up,
         description="Ask the user for a number n and print every number from 1 up "
                     "to n.",
         predict=[{"n": 5}, {"n": 1}, {"n": 3}]),

    DRAW(times_table,
         description="Ask the user for a number n and print its multiplication "
                     "table, from n × 1 up to n × 10.",
         predict=[{"n": 7}, {"n": 3}]),

    DRAW(sum_1_to_n,
         description="Ask the user for a number n and print the total 1 + 2 + 3 + "
                     "… + n.",
         predict=[{"n": 4}, {"n": 1}, {"n": 6}]),

    DRAW(count_digits,
         description="Ask the user for a whole number n and print how many digits "
                     "it has.",
         predict=[{"n": 4072}, {"n": 538}, {"n": 9}]),

    DRAW(print_evens,
         description="Ask the user for a number n and print only the even numbers "
                     "from 1 up to n.",
         predict=[{"n": 8}, {"n": 5}, {"n": 1}]),
]
