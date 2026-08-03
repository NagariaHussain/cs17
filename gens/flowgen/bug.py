"""Debug problems — one deliberate mistake planted in a correct algorithm.

The CORRECT algorithm stays the single source of truth. A bug is a tiny
declarative mutation (`wrong_cond("i <= n", "i < n")`, `missing("i = i + 1")`,
…) applied to a deep copy of it, so everything the sheet shows is derived from
the pair and nothing about the bug is written twice:

  buggy flowchart      render the mutated copy
  "should print"       run the correct algorithm on the given inputs
  "actually prints"    run the buggy copy on the same inputs
  the fix (answer key) each mutator reports the box it touched and what that box
                       should say — again read off the correct algorithm

A fix is returned as a small tuple, ("replace", wrong, right) and friends, that
`latex.py` turns into a sentence; see `FIXES` below.

Every mutator asserts it matched exactly one statement, and `apply_bug` asserts
the pseudocode actually changed — so a bug can never silently fail to apply
(which would print a "buggy" flowchart that is in fact correct).
"""

from __future__ import annotations

import copy

from .algo import (Algorithm, Assign, If, Input, Output, Runaway, While,
                   display_expr, pseudocode_lines, run)

# The fix shapes a mutator can report (rendered by latex._fix_text):
#   ("replace", wrong_box, right_box)      a box says the wrong thing
#   ("missing", box, where)                a box was left out
#   ("moved",   box, where)                a box sits inside the loop, not after
#   ("swapped", condition, yes_box, no_box) the Yes/No arms are the wrong way round
FIXES = ("replace", "missing", "moved", "swapped")


# ---- locating a statement ----------------------------------------------------

def _walk(stmts, parent=None):
    """Yield (container_list, index, stmt, parent) for every statement,
    depth-first; `parent` is the enclosing If/While, or None at the top."""
    for i, s in enumerate(stmts):
        yield stmts, i, s, parent
        if isinstance(s, If):
            yield from _walk(s.then, s)
            yield from _walk(s.els, s)
        elif isinstance(s, While):
            yield from _walk(s.body, s)


def source_line(s) -> str:
    """The pseudocode text of one simple statement, in AUTHORED form (no
    is/is-not display translation) — what a mutator's locator is matched
    against, so worksheets can say missing("i = i + 1")."""
    if isinstance(s, Input):
        return f"read {s.var}"
    if isinstance(s, Assign):
        return f"{s.var} = {s.expr}"
    if isinstance(s, Output):
        return f"print {s.expr}"
    if isinstance(s, If):
        return f"if {s.cond}"
    if isinstance(s, While):
        return f"while {s.cond}"
    raise AssertionError(s)


def _one(stmts, pred, what):
    """The single statement matching `pred`, as (container, index, stmt, parent)."""
    hits = [h for h in _walk(stmts) if pred(h[2])]
    assert hits, f"no statement matches {what}"
    assert len(hits) == 1, f"{len(hits)} statements match {what} — be more specific"
    return hits[0]


def _where(parent) -> str:
    """Where in the chart a box sits, for the answer key's sentence."""
    if isinstance(parent, While):
        return "inside the loop"
    if isinstance(parent, If):
        return "in the decision's branch"
    return ""


# ---- the mutators ------------------------------------------------------------
# Each returns a function that mutates a statement tree in place AND returns the
# fix (see FIXES). They are the mistakes beginners actually make, one per kind:

def wrong_cond(old: str, new: str):
    """A decision (if/while) tests the wrong thing — >= vs >, and vs or, an
    off-by-one loop condition, a reversed comparison."""
    def mutate(body):
        _, _, s, _p = _one(body, lambda s: isinstance(s, (If, While)) and s.cond == old,
                           f"the condition {old!r}")
        s.cond = new
        return ("replace", display_expr(new), display_expr(old))
    return mutate


def wrong_assign(var: str, old: str, new: str):
    """A box computes/initialises the wrong value (sum = 1 instead of 0,
    sum = x instead of sum + x)."""
    def mutate(body):
        _, _, s, _p = _one(body, lambda s: isinstance(s, Assign) and s.var == var
                           and s.expr == old, f"the assignment {var} = {old!r}")
        s.expr = new
        return ("replace", f"{var} = {display_expr(new)}",
                f"{var} = {display_expr(old)}")
    return mutate


def wrong_print(old: str, new: str):
    """The program prints the wrong thing (the total instead of the average,
    the counter instead of the result)."""
    def mutate(body):
        _, _, s, _p = _one(body, lambda s: isinstance(s, Output) and s.expr == old,
                           f"the output {old!r}")
        s.expr = new
        return ("replace", f"print {display_expr(new)}",
                f"print {display_expr(old)}")
    return mutate


def swap_branches(cond: str):
    """The Yes and No arms of a decision are the wrong way round."""
    def mutate(body):
        _, _, s, _p = _one(body, lambda s: isinstance(s, If) and s.cond == cond,
                           f"the if {cond!r}")
        assert s.els, "swap_branches needs an if with an else"
        yes, no = source_line(s.then[0]), source_line(s.els[0])
        s.then, s.els = s.els, s.then
        return ("swapped", display_expr(cond), display_expr(yes), display_expr(no))
    return mutate


def missing(line: str):
    """A box is left out altogether — classically the counter update inside a
    loop, which makes the loop run forever."""
    def mutate(body):
        container, idx, stmt, parent = _one(body, lambda s: source_line(s) == line,
                                            f"the box {line!r}")
        container.pop(idx)
        return ("missing", display_expr(source_line(stmt)), _where(parent))
    return mutate


def move_into_loop(line: str):
    """A box that belongs AFTER the loop was drawn inside it — so it happens
    every time round instead of once at the end."""
    def mutate(body):
        container, idx, stmt, _p = _one(body, lambda s: source_line(s) == line,
                                        f"the box {line!r}")
        assert idx > 0 and isinstance(container[idx - 1], While), \
            f"{line!r} does not directly follow a loop"
        loop = container[idx - 1]
        container.pop(idx)
        loop.body.append(stmt)
        return ("moved", display_expr(source_line(stmt)), "after the loop")
    return mutate


# ---- applying it ------------------------------------------------------------

def apply_bug(algo: Algorithm, bug):
    """(buggy copy, fix) — the algorithm with the bug planted in it, and what has
    to be put right (the original algorithm is untouched)."""
    broken = Algorithm(algo.title, copy.deepcopy(algo.body))
    fix = bug(broken.body)
    assert fix and fix[0] in FIXES, f"mutator returned no fix: {fix!r}"
    assert pseudocode_lines(broken) != pseudocode_lines(algo), \
        f"bug did not change {algo.title!r}"
    return broken, fix


def outcome(algo: Algorithm, inputs: dict, *, step_limit: int = 120):
    """(outputs, never_stops) — what the program prints on `inputs`.

    A buggy algorithm may loop forever; we cut it off at `step_limit` and report
    what it had printed by then, since "prints 1, 1, 1, … and never stops" is
    exactly the symptom the student has to explain."""
    try:
        _, _, outputs = run(algo, inputs, step_limit=step_limit)
        return outputs, False
    except Runaway as e:
        return e.outputs, True
