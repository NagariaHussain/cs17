"""Boolean expression model — the single source of truth for a problem.

A problem is authored as ONE expression. From that one tree we derive:
  - the gate diagram        (-> schemdraw, see diagram.py)
  - the displayed formula   (-> engineering LaTeX, see latex.py)
  - the truth table         (-> evaluate(), below)

Keeping NAND/NOR/XOR/XNOR as first-class gate nodes (instead of letting a
CAS rewrite them into AND/OR/NOT) means the drawn gate, the printed formula,
and the table always match what the student is asked to reason about.
"""

from __future__ import annotations

import ast as _pyast
from dataclasses import dataclass

# Gate operators we support as real gates.
_OPS = {"NOT", "AND", "OR", "NAND", "NOR", "XOR", "XNOR"}


@dataclass(frozen=True)
class Var:
    name: str


@dataclass(frozen=True)
class Gate:
    op: str
    args: tuple  # tuple[Var | Gate, ...]

    def __post_init__(self):
        assert self.op in _OPS, f"unknown gate {self.op!r}"
        if self.op == "NOT":
            assert len(self.args) == 1, "NOT takes one input"
        else:
            assert len(self.args) >= 2, f"{self.op} takes >= 2 inputs"


Expr = Var | Gate


# ---- constructors (handy for authoring problems in Python) -------------------

def V(name: str) -> Var:
    return Var(name)


def NOT(x: Expr) -> Gate:
    return Gate("NOT", (x,))


def _mk(op):
    def f(*args: Expr) -> Gate:
        return Gate(op, tuple(args))
    return f


AND, OR, NAND, NOR, XOR, XNOR = (_mk(o) for o in ("AND", "OR", "NAND", "NOR", "XOR", "XNOR"))


# ---- string DSL: parse("(a & b) | ~c") or "nand(a & b, c)" -------------------
#
# & = AND   | = OR   ~ = NOT   ^ = XOR   and functions nand(), nor(), xnor().
# Python operator precedence (~ > & > ^ > |) already matches boolean precedence;
# use parentheses when in doubt.

_CALLS = {"and_": "AND", "or_": "OR", "nand": "NAND", "nor": "NOR",
          "xor": "XOR", "xnor": "XNOR", "not_": "NOT"}


def parse(src: str) -> Expr:
    """Parse a boolean expression string into an Expr tree."""
    tree = _pyast.parse(src, mode="eval").body
    return _convert(tree)


def _convert(node) -> Expr:
    if isinstance(node, _pyast.Name):
        return Var(node.id)
    if isinstance(node, _pyast.BinOp):
        left, right = _convert(node.left), _convert(node.right)
        if isinstance(node.op, _pyast.BitAnd):
            return Gate("AND", (left, right))
        if isinstance(node.op, _pyast.BitOr):
            return Gate("OR", (left, right))
        if isinstance(node.op, _pyast.BitXor):
            return Gate("XOR", (left, right))
    if isinstance(node, _pyast.UnaryOp) and isinstance(node.op, _pyast.Invert):
        return Gate("NOT", (_convert(node.operand),))
    if isinstance(node, _pyast.Call) and isinstance(node.func, _pyast.Name):
        op = _CALLS.get(node.func.id)
        if op:
            return Gate(op, tuple(_convert(a) for a in node.args))
    raise ValueError(f"unsupported syntax in expression: {_pyast.dump(node)}")


# ---- evaluation & variables --------------------------------------------------

def variables(e: Expr) -> list[str]:
    """Sorted list of distinct variable names in the expression."""
    seen: set[str] = set()

    def walk(n):
        if isinstance(n, Var):
            seen.add(n.name)
        else:
            for a in n.args:
                walk(a)

    walk(e)
    return sorted(seen)


def evaluate(e: Expr, env: dict[str, bool]) -> bool:
    if isinstance(e, Var):
        return bool(env[e.name])
    vals = [evaluate(a, env) for a in e.args]
    op = e.op
    if op == "NOT":
        return not vals[0]
    if op == "AND":
        return all(vals)
    if op == "OR":
        return any(vals)
    if op == "NAND":
        return not all(vals)
    if op == "NOR":
        return not any(vals)
    if op == "XOR":
        r = False
        for v in vals:
            r ^= v
        return r
    if op == "XNOR":
        r = False
        for v in vals:
            r ^= v
        return not r
    raise AssertionError(op)


def truth_table(e: Expr, vars_: list[str] | None = None) -> tuple[list[str], list[tuple[list[int], int]]]:
    """Return (var_names, rows) where each row is (input_bits, output_bit)."""
    vars_ = vars_ or variables(e)
    rows = []
    for i in range(2 ** len(vars_)):
        bits = [(i >> (len(vars_) - 1 - k)) & 1 for k in range(len(vars_))]
        env = dict(zip(vars_, (bool(b) for b in bits)))
        out = int(evaluate(e, env))
        rows.append((bits, out))
    return vars_, rows
