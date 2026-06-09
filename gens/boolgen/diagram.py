"""Render an Expr to a gate diagram via schemdraw.

We translate our Expr tree into the infix string that schemdraw's logic parser
understands, then let schemdraw auto-lay-out the gates. Saving to .pdf gives a
vector figure for the LaTeX worksheet; .png/.svg are for reuse elsewhere.
"""

from __future__ import annotations

import schemdraw
from schemdraw.parsing import logicparse

from .expr import Expr, Gate, Var

# Lighter strokes than schemdraw's default (lw=2.0), so gates read like a
# textbook rather than thick & dark. Diagrams are embedded at natural size.
schemdraw.config(lw=1.0, fontsize=14)

# Our op name -> schemdraw infix keyword
_INFIX = {"AND": "and", "OR": "or", "NAND": "nand", "NOR": "nor",
          "XOR": "xor", "XNOR": "xnor"}


def to_logic_string(e: Expr) -> str:
    """Translate an Expr into a schemdraw logicparse expression string."""
    if isinstance(e, Var):
        return e.name
    if e.op == "NOT":
        return f"not ({to_logic_string(e.args[0])})"
    kw = _INFIX[e.op]
    # left-fold n-ary gates into binary, fully parenthesised
    parts = [to_logic_string(a) for a in e.args]
    acc = parts[0]
    for p in parts[1:]:
        acc = f"({acc} {kw} {p})"
    return acc


def render(e: Expr, path_stem: str, *, outlabel: str = "Y", gateH: float = 1.25,
           formats=("pdf", "png", "svg")):
    """Draw the diagram for `e` and save `path_stem.<fmt>` for each format.

    `gateH` is the per-gate height; the default (larger than schemdraw's 0.75)
    spreads stacked gates apart so inverters/inputs don't overlap or cross.
    Returns the schemdraw drawing (already built).
    """
    d = logicparse(to_logic_string(e), gateH=gateH, outlabel=outlabel)
    for fmt in formats:
        d.save(f"{path_stem}.{fmt}")
    return d
