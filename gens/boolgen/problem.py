"""A worksheet problem = an expression + which direction the student works.

Three kinds, all derived from the same single source expression:

  DIAGRAM     given the gate diagram  -> write the expression + draw truth table
  CIRCUIT     given the expression    -> draw the logic-gate circuit
  TRUTHTABLE  given the expression    -> draw the truth table   (keep <= 3 vars)

A bare expression in a worksheet defaults to DIAGRAM.
"""

from __future__ import annotations

from dataclasses import dataclass

from .expr import Expr

KINDS = ("diagram", "circuit", "truthtable")


@dataclass
class Problem:
    expr: Expr
    kind: str = "diagram"
    title: str = ""

    def __post_init__(self):
        assert self.kind in KINDS, f"unknown kind {self.kind!r}"


def DIAGRAM(e: Expr, title: str = "") -> Problem:
    return Problem(e, "diagram", title)


def CIRCUIT(e: Expr, title: str = "") -> Problem:
    return Problem(e, "circuit", title)


def TRUTHTABLE(e: Expr, title: str = "") -> Problem:
    return Problem(e, "truthtable", title)
