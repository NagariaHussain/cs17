"""A pocket spreadsheet: enough of Calc to work out what a formula shows.

A CALC question prints a grid of data and a formula, and asks the student what
appears in the cell. The formula is the only thing authored -- the answer is
obtained by evaluating it against the same grid the paper prints, so a question
can never ask for a value the printed data does not support (a typo in a price
changes the answer, it does not leave the paper disagreeing with itself).

Supported, because that is what the questions use:

    =SUM(B2:B7)   =AVERAGE(...)  =MAX(...)  =MIN(...)  =COUNT(...)
    =IF(<test>, <value if true>, <value if false>)
    =SUMIF(B2:B7, ">100")            add only the cells that match
    =SUMIF(A2:A7, "Pen", B2:B7)      test one range, add the matching cells
                                     of another
    a test is one cell against a number: B2 > 100, B4 <= 50, B3 = 15
    a criterion is Calc's own quoted form: ">100", "<=50", "Pen" (no
    operator means "equal to")
    a value is a "quoted string", a number, a cell reference, or a nested call

Anything else raises, so an unsupported formula fails the build rather than
shipping unchecked.
"""

from __future__ import annotations

import re

_CELL = re.compile(r"^([A-Z]+)([0-9]+)$")
_RANGE = re.compile(r"^([A-Z]+[0-9]+):([A-Z]+[0-9]+)$")
_CALL = re.compile(r"^([A-Z]+)\((.*)\)$", re.S)
_TEST = re.compile(r"^(.+?)(<=|>=|<>|=|<|>)(.+)$")

_AGG = {
    "SUM": sum,
    "AVERAGE": lambda vs: sum(vs) / len(vs),
    "MAX": max,
    "MIN": min,
    "COUNT": len,
}


def _cell(ref: str) -> tuple:
    m = _CELL.match(ref.strip().upper())
    assert m, f"not a cell reference: {ref!r}"
    return m.group(1), int(m.group(2))


def _split_args(s: str) -> list:
    """Split on the commas that separate arguments -- not the ones inside a
    nested call or a quoted string."""
    args, depth, quoted, cur = [], 0, False, ""
    for ch in s:
        if ch == '"':
            quoted = not quoted
        if not quoted:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            elif ch == "," and depth == 0:
                args.append(cur)
                cur = ""
                continue
        cur += ch
    args.append(cur)
    return [a.strip() for a in args]


def _range_cells(spec: str) -> list:
    m = _RANGE.match(spec.strip().upper())
    assert m, f"not a range: {spec!r}"
    (c0, r0), (c1, r1) = _cell(m.group(1)), _cell(m.group(2))
    cols = [chr(c) for c in range(ord(min(c0, c1)), ord(max(c0, c1)) + 1)]
    return [(c, r) for c in cols for r in range(min(r0, r1), max(r0, r1) + 1)]


def evaluate(formula: str, values: dict):
    """What `formula` shows, given `values` keyed by (column letter, row)."""
    return _eval(formula.strip().lstrip("="), values)


def _eval(s: str, values: dict):
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    call = _CALL.match(s)
    if call:
        name, inner = call.group(1).upper(), call.group(2)
        if name == "IF":
            args = _split_args(inner)
            assert len(args) == 3, f"IF takes three arguments: {s!r}"
            branch = args[1] if _test(args[0], values) else args[2]
            return _eval(branch, values)
        if name == "SUMIF":
            return _sumif(_split_args(inner), values)
        assert name in _AGG, f"unsupported function {name!r}"
        cells = [_eval_cell(c, values) for c in _range_cells(inner)]
        return _AGG[name](cells)
    if _CELL.match(s.upper()):
        return _eval_cell(_cell(s), values)
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        raise AssertionError(f"cannot evaluate {s!r}")


def _eval_cell(ref: tuple, values: dict):
    assert ref in values, f"cell {ref[0]}{ref[1]} is empty"
    return values[ref]


def _sumif(args: list, values: dict):
    """SUMIF(range, criterion) or SUMIF(range, criterion, sum_range).

    The criterion is tested against each cell of `range`; what gets added is
    the matching cell of `sum_range` when one is given, and of `range` itself
    when it is not. The two ranges are walked in step, so they must be the same
    length -- Calc lines them up by position, not by address."""
    assert len(args) in (2, 3), f"SUMIF takes two or three arguments: {args!r}"
    tested = _range_cells(args[0])
    added = _range_cells(args[2]) if len(args) == 3 else tested
    assert len(tested) == len(added), "SUMIF ranges are different sizes"
    op, wanted = _criterion(args[1], values)
    total = 0
    for probe, target in zip(tested, added):
        if _compare(_eval_cell(probe, values), op, wanted):
            total += _eval_cell(target, values)
    return total


def _criterion(s: str, values: dict) -> tuple:
    """Calc writes a SUMIF criterion as one string, ">100" or "Pen"; split it
    into the operator and the value it is compared against."""
    s = s.strip()
    if s.startswith('"') and s.endswith('"'):
        s = s[1:-1].strip()
    for op in ("<=", ">=", "<>", "<", ">", "="):
        if s.startswith(op):
            return op, _eval(s[len(op):], values)
    try:
        return "=", _eval(s, values)
    except AssertionError:
        return "=", s          # a bare word, matched as text


def _compare(left, op: str, right) -> bool:
    return {"<": left < right, ">": left > right, "<=": left <= right,
            ">=": left >= right, "=": left == right, "<>": left != right}[op]


def _test(s: str, values: dict) -> bool:
    m = _TEST.match(s.strip())
    assert m, f"not a comparison: {s!r}"
    left, op, right = _eval(m.group(1), values), m.group(2), _eval(m.group(3), values)
    return {"<": left < right, ">": left > right, "<=": left <= right,
            ">=": left >= right, "=": left == right, "<>": left != right}[op]
