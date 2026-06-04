"""Flowchart Worksheet — simple algorithms.

Each algorithm is authored once; the flowchart, pseudocode, and trace table are
all derived from it. Problem types:

  TRACE(algo, {...})    given the flowchart + inputs -> fill the trace table
  DRAW(algo)            given the pseudocode          -> draw the flowchart
  OUTPUTS(algo, [...])  given the flowchart           -> find the output per input
"""

from flowgen import Algorithm, read, assign, out, If, While, TRACE, DRAW, OUTPUTS

TITLE = "Flowchart Worksheet"

absolute = Algorithm("Absolute value", [
    read("n"),
    If("n < 0", [assign("n", "-n")]),
    out("n"),
])

sum_1_to_n = Algorithm("Sum 1..n", [
    read("n"),
    assign("sum", "0"),
    assign("i", "1"),
    While("i <= n", [
        assign("sum", "sum + i"),
        assign("i", "i + 1"),
    ]),
    out("sum"),
])

sum_even = Algorithm("Sum of even numbers 1..n", [
    read("n"),
    assign("sum", "0"),
    assign("i", "1"),
    While("i <= n", [
        If("i % 2 == 0", [assign("sum", "sum + i")]),
        assign("i", "i + 1"),
    ]),
    out("sum"),
])

count_multiples = Algorithm("Count of multiples of 3", [
    read("n"),
    assign("count", "0"),
    assign("i", "1"),
    While("i <= n", [
        If("i % 3 == 0", [assign("count", "count + 1")]),
        assign("i", "i + 1"),
    ]),
    out("count"),
])

count_digits = Algorithm("Count of digits", [
    read("n"),
    assign("count", "0"),
    While("n > 0", [
        assign("count", "count + 1"),
        assign("n", "n // 10"),
    ]),
    out("count"),
])

PROBLEMS = [
    OUTPUTS(absolute, [{"n": 7}, {"n": -4}, {"n": 0}, {"n": -19}],
            followup="Can you tell what this algorithm is doing?"),
    TRACE(sum_1_to_n, {"n": 4}),
    TRACE(sum_even, {"n": 5}),
    TRACE(count_multiples, {"n": 7}),
    TRACE(count_digits, {"n": 472}),
]
