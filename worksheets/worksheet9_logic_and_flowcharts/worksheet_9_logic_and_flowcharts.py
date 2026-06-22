"""Worksheet 9 — a mixed review: logic gates AND flowchart tracing.

This sheet pulls together the two strands of the course so far. It is hosted by
boolgen (Boolean algebra is the lead topic) but, like the binary sheets host
revision questions, it also mixes in a couple of flowgen flowchart-tracing
problems — boolgen reuses flowgen's own renderer for those.

Boolean problem kinds used here (all authored from ONE expression, so the table,
the formula, and the circuit can never disagree):

  FROMTABLE   given the truth table   -> write the expression + draw the circuit
  DIAGRAM     given the gate diagram  -> write the expression + draw truth table

Syntax:  &=AND  |=OR  ~=NOT  ^=XOR   ;  nand(a,b) nor(a,b) xnor(a,b)

The two flowcharts are presented neutrally ("trace this flowchart"); each one's
real-world use is only named afterwards, in the `reveal` shown below the table.
"""

from gens.boolgen import parse, DIAGRAM, FROMTABLE
from gens.flowgen import Algorithm, read, assign, out, If, While, TRACE

TITLE = "Worksheet 9: Logic Gates \\& Flowchart Tracing"

INDEX_NOTE = ("Reminder: the items of a list have positions counted from 0, so "
              "the list [60, 75, 50] has 3 items in positions 0, 1, 2 — "
              "arr[i] means the item at position i, so arr[0] is the first item.")

# --- the two flowcharts (authored once; flowchart + trace table both derived) --

# A doubly-nested counting loop: for every pair (i, j) with i < j, bump a counter.
# Real-world: this is how you count the number of distinct PAIRS in a group —
# handshakes among n people, or direct links in a fully-connected network.
count_pairs = Algorithm("Count the pairs among n items", [
    read("n"),
    assign("count", "0"),
    assign("i", "1"),
    While("i <= n", [
        assign("j", "i + 1"),
        While("j <= n", [
            assign("count", "count + 1"),
            assign("j", "j + 1"),
        ]),
        assign("i", "i + 1"),
    ]),
    out("count"),
])

# Two SEPARATE loops in one algorithm (a two-pass algorithm): the first loop
# walks the whole list to total it up and work out the average; the second loop
# walks the same list again, counting how many items beat that average.
# Real-world: counting how many values are above the average — e.g. how many
# students scored above the class average.
above_average = Algorithm("How many numbers are above the average", [
    assign("sum", "0"),
    assign("i", "0"),
    While("i < 4", [
        assign("sum", "sum + arr[i]"),
        assign("i", "i + 1"),
    ]),
    assign("avg", "sum / 4"),
    assign("count", "0"),
    assign("j", "0"),
    While("j < 4", [
        If("arr[j] > avg",
           [assign("count", "count + 1")]),
        assign("j", "j + 1"),
    ]),
    out("count"),
])

PROBLEMS = [
    # ---- Part A: truth table -> expression -> logic-gate circuit (FROMTABLE) ----
    FROMTABLE(parse("(a & ~b) | (~a & b)")),
    FROMTABLE(parse("(a & b) | (~a & ~b)")),
    FROMTABLE(parse("(a & b) | (a & c) | (b & c)")),

    # ---- Part B: logic-gate circuit -> expression -> truth table (DIAGRAM) ----
    # Each circuit has several gates (one 3-gate, then two 4-gate circuits).
    DIAGRAM(parse("(a & b) | ~c")),              # 3 gates: AND, NOT, OR
    DIAGRAM(parse("(~a & b) | (b & c)")),        # 4 gates: NOT, AND, AND, OR
    DIAGRAM(parse("(a | b) & (~a | c)")),        # 4 gates: OR, NOT, OR, AND (product of sums)

    # ---- Part C: trace the flowchart ----
    TRACE(count_pairs, {"n": 3},
          reveal="In the real world this is how you count the number of distinct "
                 "pairs in a group of n things: the number of handshakes if n "
                 "people all shake hands once, or the number of direct links in a "
                 "network where every one of n computers connects to every other. "
                 "It always works out to n × (n - 1) / 2."),

    TRACE(above_average, {"arr": (70, 90, 60, 80)},
          note=INDEX_NOTE,
          reveal="This two-pass pattern — go through the data once to measure "
                 "something overall, then go through it again to compare each "
                 "item against that measure — is everywhere in data analysis: for "
                 "example, finding how many students scored above the class "
                 "average, or how many days this month were hotter than usual."),
]
