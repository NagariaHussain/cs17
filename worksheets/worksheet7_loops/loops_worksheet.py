"""Simple Loops Worksheet — trace a loop, and draw one.

A focused first look at the core loop shapes a beginner needs: count up,
count down, accumulate, track a running value, and loop until a value crosses
a target (a tank draining below a level, an investment growing past double).
Two problem types are mixed:

  TRACE(algo, {...})  given the flowchart + inputs -> fill the trace table
  DRAW(algo, ...)     given a plain-English statement -> draw the flowchart

As in the other flowchart worksheets, each algorithm is authored once and the
flowchart, pseudocode, and trace table are all derived from the same source.
"""

from gens.flowgen import Algorithm, read, assign, out, If, While, TRACE, DRAW

TITLE = "Flowcharts III — Simple Loops"

# 1. the bare counting loop: just a counter and a print
print_1_to_n = Algorithm("Print 1 to n", [
    read("n"),
    assign("i", "1"),
    While("i <= n", [
        out("i"),
        assign("i", "i + 1"),
    ]),
])

# 2. the same counter, running the other way
countdown = Algorithm("Countdown from n to 1", [
    read("n"),
    assign("i", "n"),
    While("i >= 1", [
        out("i"),
        assign("i", "i - 1"),
    ]),
])

# 3. a fixed 10-iteration loop
times_table = Algorithm("Multiplication table of n", [
    read("n"),
    assign("i", "1"),
    While("i <= 10", [
        out("n * i"),
        assign("i", "i + 1"),
    ]),
])

# 4. an accumulator — but multiplying, not adding
factorial = Algorithm("Factorial of n", [
    read("n"),
    assign("fact", "1"),
    assign("i", "1"),
    While("i <= n", [
        assign("fact", "fact * i"),
        assign("i", "i + 1"),
    ]),
    out("fact"),
])

# 5. count-controlled: read a fixed number of values and add them up
sum_of_n = Algorithm("Sum of n numbers", [
    read("n"),
    assign("sum", "0"),
    assign("i", "1"),
    While("i <= n", [
        read("x"),
        assign("sum", "sum + x"),
        assign("i", "i + 1"),
    ]),
    out("sum"),
])

# 6. loop + a running "best so far"
largest_of_n = Algorithm("Largest of n numbers", [
    read("n"),
    read("largest"),  # take the first number as the largest so far
    assign("i", "2"),
    While("i <= n", [
        read("x"),
        If("x > largest", [assign("largest", "x")]),
        assign("i", "i + 1"),
    ]),
    out("largest"),
])

# 7. loop until a value DECAYS below a target — count the steps it takes
water_tank = Algorithm("Draining water tank", [
    read("litres"),
    assign("minutes", "0"),
    While("litres >= 1", [
        assign("litres", "litres / 2"),
        assign("minutes", "minutes + 2"),
    ]),
    out("minutes"),
])

# 8. loop until a value GROWS past a target — the mirror image of the tank
investment_doubles = Algorithm("Years for an investment to double", [
    read("p"),
    assign("amount", "p"),
    assign("years", "0"),
    While("amount < 2 * p", [
        assign("amount", "amount * 1.1"),
        assign("years", "years + 1"),
    ]),
    out("years"),
])

PROBLEMS = [
    TRACE(print_1_to_n, {"n": 5}),
    DRAW(countdown,
         description="Ask the user for a number n, then print all the numbers "
                     "from n down to 1, one at a time (so for n = 5 it prints "
                     "5, 4, 3, 2, 1)."),
    DRAW(times_table,
         description="Ask the user for a number n and print its multiplication "
                     "table from n × 1 up to n × 10 — that is, print the values "
                     "n×1, n×2, n×3, …, n×10."),
    TRACE(factorial, {"n": 5}),
    TRACE(sum_of_n, {"n": 3, "x": [10, 20, 30]},
          description="This program reads how many numbers there are (n), then "
                      "reads that many numbers one by one and prints their total."),
    DRAW(largest_of_n,
         description="Ask the user for a count n, then read n numbers one by "
                     "one and print the largest of them. (Hint: remember the "
                     "first number as the “largest so far”, then compare every "
                     "later number against it and update it when you find a "
                     "bigger one.)"),
    TRACE(water_tank, {"litres": 64},
          description="A water tank holds some litres of water. Every 2 minutes, "
                      "exactly half of the water currently in the tank drains "
                      "out. The program keeps going until less than 1 litre is "
                      "left, and prints how many minutes that took. (Notice that "
                      "the tank never becomes completely empty — can you see "
                      "why?)"),
    DRAW(investment_doubles,
         description="An investment of P rupees grows by 10% every year — so "
                     "each year the amount becomes 1.1 times what it was the "
                     "year before. Print how many years it takes for the "
                     "investment to at least double (that is, to reach 2 × P)."),
]
