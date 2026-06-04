"""Algorithm model — the single source of truth for a flowchart problem.

An algorithm is authored once as a small statement tree. From it we derive:
  - the flowchart diagram   (-> graphviz, see flowchart.py)
  - the pseudocode          (-> pseudocode_lines, below)
  - a trace table           (-> run(), below: execute on given inputs)

Expressions/conditions are plain strings (e.g. "sum + i", "n % 2 == 0"): the
SAME string is shown to the student AND evaluated by the tracer, so the diagram,
the pseudocode, and the trace can never disagree.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---- statements --------------------------------------------------------------

@dataclass
class Input:
    var: str


@dataclass
class Assign:
    var: str
    expr: str


@dataclass
class Output:
    expr: str


@dataclass
class If:
    cond: str
    then: list
    els: list = field(default_factory=list)


@dataclass
class While:
    cond: str
    body: list


# tiny constructors so worksheets read like pseudocode
def read(var: str) -> Input:
    return Input(var)


def assign(var: str, expr: str) -> Assign:
    return Assign(var, expr)


def out(expr: str) -> Output:
    return Output(expr)


@dataclass
class Algorithm:
    title: str
    body: list


# ---- pseudocode --------------------------------------------------------------

def pseudocode_lines(algo: Algorithm) -> list[tuple[int, str]]:
    """Return (indent_level, text) lines."""
    lines: list[tuple[int, str]] = []

    def emit(stmts, lvl):
        for s in stmts:
            if isinstance(s, Input):
                lines.append((lvl, f"read {s.var}"))
            elif isinstance(s, Assign):
                lines.append((lvl, f"{s.var} = {s.expr}"))
            elif isinstance(s, Output):
                lines.append((lvl, f"print {s.expr}"))
            elif isinstance(s, If):
                lines.append((lvl, f"if {s.cond}:"))
                emit(s.then, lvl + 1)
                if s.els:
                    lines.append((lvl, "else:"))
                    emit(s.els, lvl + 1)
            elif isinstance(s, While):
                lines.append((lvl, f"while {s.cond}:"))
                emit(s.body, lvl + 1)
            else:
                raise AssertionError(s)

    emit(algo.body, 0)
    return lines


def pseudocode_text(algo: Algorithm, indent: str = "    ") -> str:
    return "\n".join(indent * lvl + text for lvl, text in pseudocode_lines(algo))


# ---- tracing (execute to build the trace table) ------------------------------

_SAFE = {"__builtins__": {}}


def run(algo: Algorithm, inputs: dict, *, step_limit: int = 2000):
    """Execute the algorithm on `inputs`.

    Returns (columns, rows, outputs):
      columns : ordered variable names (by first assignment) — table columns
      rows    : list of (env_snapshot, output_this_step_or_None)
      outputs : list of all printed values, in order
    """
    env: dict = {}
    cols: list[str] = []
    rows: list[tuple[dict, object]] = []
    outputs: list = []
    steps = [0]

    def track(v):
        if v not in cols:
            cols.append(v)

    def snap(output=None):
        rows.append((dict(env), output))

    def ev(s):
        return eval(s, _SAFE, env)  # authored expressions only — not user input

    def exec_(stmts):
        for s in stmts:
            steps[0] += 1
            if steps[0] > step_limit:
                raise RuntimeError("step limit exceeded — runaway loop?")
            if isinstance(s, Input):
                env[s.var] = inputs[s.var]
                track(s.var)
                snap()
            elif isinstance(s, Assign):
                env[s.var] = ev(s.expr)
                track(s.var)
                snap()
            elif isinstance(s, Output):
                val = ev(s.expr)
                outputs.append(val)
                snap(val)
            elif isinstance(s, If):
                exec_(s.then if ev(s.cond) else s.els)
            elif isinstance(s, While):
                while ev(s.cond):
                    exec_(s.body)
            else:
                raise AssertionError(s)

    exec_(algo.body)
    return cols, rows, outputs
