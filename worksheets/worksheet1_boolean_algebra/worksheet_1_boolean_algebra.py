"""Boolean Algebra Worksheet — all questions in one sheet.

Each problem is ONE expression; the diagram, formula, and truth table are all
derived from it, so they can't drift out of sync. Three problem types:

  parse(...)            given the circuit  -> write expression + draw truth table
  CIRCUIT(parse(...))   given the expression -> draw the logic-gate circuit
  TRUTHTABLE(parse(...)) given the expression -> draw the truth table  (<= 3 vars)

Syntax:  &=AND  |=OR  ~=NOT  ^=XOR   ;  nand(a,b) nor(a,b) xnor(a,b)
"""

from gens.boolgen import parse, CIRCUIT, TRUTHTABLE

TITLE = "Worksheet 1: Boolean Algebra"

# show the XOR-identity reminder box on the worksheet (this is the sheet that
# first introduces XOR; later sheets have students derive it themselves)
XOR_REMINDER = True

PROBLEMS = [
    # ---- Part A: read the circuit -> write the expression + draw truth table ----
    parse("(a & b) | ~c"),
    parse("(a & b) | (b & c) | (a & c)"),
    parse("a ^ b"),
    parse("(a ^ b) ^ c"),
    parse("(a & ~b) | (~a & b)"),
    # more sum-of-products with complemented inputs (same family as the one above)
    parse("(a & b) | (~a & ~b)"),
    parse("(a & ~b) | (b & ~c)"),
    parse("(~a & b & c) | (a & ~c)"),
    parse("nand(a, b)"),
    parse("nor(a, b)"),
    parse("nor(a & b, ~c)"),
    parse("~(~a & ~b)"),
    parse("nand(a, ~b)"),
    parse("~(~a | b)"),
    parse("nand(nand(a, b), nand(c, d))"),

    # ---- Part B: read the expression -> draw the logic-gate circuit ----
    CIRCUIT(parse("a & (b | c)")),
    CIRCUIT(parse("~(a & b) | c")),
    CIRCUIT(parse("(a | b) & (a | c)")),
    CIRCUIT(parse("a ^ (b & c)")),

    # ---- Part C: read the expression -> draw the truth table (<= 3 vars) ----
    TRUTHTABLE(parse("(a & b) | c")),
    TRUTHTABLE(parse("a ^ b ^ c")),
    TRUTHTABLE(parse("~(a | b) & c")),
    TRUTHTABLE(parse("(a & ~b) | (~a & c)")),
]
