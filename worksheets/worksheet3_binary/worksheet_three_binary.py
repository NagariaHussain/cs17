"""Worksheet 3 — binary numbers, with Boolean-algebra & flowchart revision.

Mostly binary (convert to decimal; decode ASCII messages), with two Boolean
questions and one flowchart trace mixed in as revision of earlier worksheets.

Each problem is still authored once from a single source of truth. The binary
problems are bingen's own; the revision problems are ordinary boolgen / flowgen
problem objects — bingen.build reuses those generators' renderers to typeset
them, so nothing is duplicated.

  bingen   TODECIMAL("1011", ...)   binary -> decimal
  bingen   DECODE("HI")             ASCII codes in binary -> message
  boolgen  DIAGRAM(parse("..."))    gate diagram -> expression + truth table
  boolgen  TRUTHTABLE(parse("...")) expression  -> truth table
  flowgen  TRACE(algo, {...})       flowchart   -> completed trace table
"""

from gens.bingen import TODECIMAL, TOBINARY, DECODE
from gens.boolgen import parse, DIAGRAM, TRUTHTABLE
from gens.flowgen import Algorithm, read, assign, out, If, While, TRACE

TITLE = "Worksheet 3: Binary"

# Revision flowchart: a few conditional blocks inside one loop (same digit-by-
# digit shape as "reverse the digits" on Worksheet 2, but counting instead).
digit_stats = Algorithm("Counting even and large digits", [
    read("n"),
    assign("evens", "0"),
    assign("big", "0"),
    While("n > 0", [
        assign("d", "n % 10"),
        If("d % 2 == 0", [assign("evens", "evens + 1")]),
        If("d > 5", [assign("big", "big + 1")]),
        assign("n", "n // 10"),
    ]),
    out("evens"),
    out("big"),
])

PROBLEMS = [
    # ---- binary -> decimal ----
    TODECIMAL("1011", "1100", "0111", "1010",
              note="Hint: the four place values are 8, 4, 2, 1. Add up the "
                   "place values wherever there is a 1."),
    TODECIMAL("10010", "100000", "111111", "101101"),
    TODECIMAL("01000001", "00101010", "10000000", "11111111",
              note="With 8 bits the place values are 128, 64, 32, 16, 8, 4, 2, 1."),

    # ---- decimal -> binary (the reverse) ----
    TOBINARY(6, 19, 42, 100,
             note="Hint: find the largest place value (…, 32, 16, 8, 4, 2, 1) "
                  "that fits, subtract it, and repeat with what's left."),

    # ---- revision: read the gate diagram (from Worksheet 1) ----
    DIAGRAM(parse("(a & b) | ~c")),

    # ---- decode the ASCII message ----
    DECODE("CS17",
           description="The digit characters 0–9 are NOT the same as the numbers "
                       "0–9 — each has its own ASCII code."),
    DECODE("binary",
           description="Decode the secret word. Watch the capitalisation — "
                       "uppercase and lowercase letters have different codes."),

    # ---- revision: draw the truth table (from Worksheet 1) ----
    TRUTHTABLE(parse("a ^ (b & c)")),

    # ---- revision: trace the flowchart (from Worksheet 2) ----
    TRACE(digit_stats, {"n": 6391},
          note="Reminder: n % 10 is the last digit of n, and n // 10 removes it "
               "(e.g. 6391 % 10 = 1 and 6391 // 10 = 639)."),
]
