"""Bridge to sympy for simplification (e.g. De Morgan).

We keep our own Expr as the source of truth for *drawing*, but borrow sympy to
compute a minimal equivalent form for the answer key. For De Morgan problems —
NAND/NOR and bubble-pushing — sympy's DNF simplification yields exactly the
"pushed-through" form students should arrive at.
"""

from __future__ import annotations

import sympy
from sympy.logic.boolalg import And, Not, Or, Xor, simplify_logic

from .expr import Expr, Gate, Var


def to_sympy(e: Expr):
    if isinstance(e, Var):
        return sympy.Symbol(e.name)
    args = [to_sympy(a) for a in e.args]
    op = e.op
    if op == "NOT":
        return ~args[0]
    if op == "AND":
        return And(*args)
    if op == "OR":
        return Or(*args)
    if op == "NAND":
        return ~And(*args)
    if op == "NOR":
        return ~Or(*args)
    if op == "XOR":
        return Xor(*args)
    if op == "XNOR":
        return ~Xor(*args)
    raise AssertionError(op)


def from_sympy(s) -> Expr:
    if isinstance(s, sympy.Symbol):
        return Var(s.name)
    if isinstance(s, Not):
        return Gate("NOT", (from_sympy(s.args[0]),))
    if isinstance(s, And):
        return Gate("AND", tuple(from_sympy(a) for a in s.args))
    if isinstance(s, Or):
        return Gate("OR", tuple(from_sympy(a) for a in s.args))
    if isinstance(s, Xor):
        return Gate("XOR", tuple(from_sympy(a) for a in s.args))
    raise ValueError(f"cannot convert sympy node {s!r}")


def simplify(e: Expr) -> Expr:
    """Return a minimal sum-of-products equivalent of `e`."""
    return from_sympy(simplify_logic(to_sympy(e), form="dnf"))
