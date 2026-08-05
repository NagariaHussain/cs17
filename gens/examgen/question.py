"""An exam question, and the parts a paper is divided into.

A paper module holds PARTS; each PART holds questions, numbered continuously
across the whole paper. A question is one of:

    Q          plain text
    SHORT      a question answered in a sentence or two
    MCQ        text + options; the student picks one
    BOOL       a Boolean expression (boolgen) -> truth table / logic circuit
    TRACE      a flowgen problem shown as a flowchart -> fill the trace table
    DRAW       an algorithm stated in English -> write it, then draw it
    DEBUG      a flowchart with N planted mistakes -> find them
    GATEMCQ    a gate diagram + expression options -> pick the right expression
    SHEET      a spreadsheet grid with a block of cells shaded -> name the range
    TBD        a placeholder for a question not written yet

The paper carries no writing space (students answer on a separate sheet), so a
question is its stem plus whatever material it needs -- a chart, an expression,
a symptom table -- and nothing else.

The flowchart questions carry a real flowgen `Algorithm`, so the chart the
student sees, the trace table's columns and the "should print / actually
prints" table are all derived by running that one algorithm — the exam can
never disagree with itself. Same for BOOL: one boolgen `Expr` per question.

No answer key is produced (an exam paper ships alone), so `answer=` on an MCQ
is a note to the setter, never rendered.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass, field

from ..flowgen.algo import Algorithm, pseudocode_lines
from . import calc as _calc

KINDS = ("text", "short", "mcq", "bool", "trace", "draw", "debug",
         "sheet", "calc", "tbd")


@dataclass
class DebugSpec:
    """A flowchart with mistakes planted in it.

    `algo` is the CORRECT algorithm and `broken` is a copy with every bug in
    `bugs` applied (flowgen's own mutators, see gens/flowgen/bug.py). Both are
    kept: the sheet runs the correct one for "should print" and the broken one
    for "actually prints", so the symptom is derived, never hand-written.
    """
    algo: Algorithm
    broken: Algorithm
    cases: list
    description: str
    n_bugs: int
    note: str = ""


@dataclass
class CalcSpec:
    """A spreadsheet with data in it, and formulas to work out by hand.

    `values` is what the grid prints, keyed by (column letter, row); `asks` is
    a list of (cell, formula, answer). The answer is EVALUATED against the same
    `values` (see calc.py), never typed in, so the grid and the answer cannot
    drift apart.
    """
    cols: list
    rows: list
    values: dict        # {(column letter, row): text or number}
    asks: list          # [(cell, formula, answer)] -- the answer is not printed


@dataclass
class SheetSpec:
    """A spreadsheet grid with one rectangular selection shaded.

    The range string ("B2:C3") is the single source: it decides which cells are
    shaded AND it is the answer, so the picture can never disagree with what is
    being asked for.
    """
    cols: list          # column letters shown, e.g. ["A", ..., "F"]
    rows: list          # row numbers shown, e.g. [1, ..., 6]
    selected: set       # {(column letter, row number)} -- shaded
    cell_range: str     # the answer, e.g. "B2:C3"; never rendered


def _cell(ref: str) -> tuple:
    """"B2" -> ("B", 2)."""
    letters = "".join(ch for ch in ref if ch.isalpha()).upper()
    digits = "".join(ch for ch in ref if ch.isdigit())
    assert letters and digits, f"not a cell reference: {ref!r}"
    return letters, int(digits)


@dataclass
class Question:
    kind: str
    marks: int | None = None
    text: str = ""
    options: tuple = ()
    answer: object = None   # setter's note; never rendered
    note: str = ""
    payload: object = None  # flowgen Problem / DebugSpec / boolgen Expr
    subparts: tuple = ()    # extra (label, text) prompts, rendered under the stem
    ask: str = ""           # BOOL: "truthtable" | "circuit"
    cases: tuple = ()       # BOOL: variable assignments to evaluate for
    algorithm_first: bool = False  # DRAW: write the algorithm before the chart
    with_table: bool = True # BOOL circuit: also ask for the truth table

    def __post_init__(self):
        assert self.kind in KINDS, f"unknown question kind {self.kind!r}"

    @property
    def figure_algo(self) -> Algorithm | None:
        """The algorithm whose flowchart must be rendered for this question
        (None when the student is the one drawing it)."""
        if self.kind == "trace":
            return self.payload.shown_algo
        if self.kind == "debug":
            return self.payload.broken
        return None

    @property
    def figure_expr(self):
        """The boolgen expression whose gate diagram must be drawn (GATEMCQ)."""
        return self.payload if self.kind == "mcq" else None


@dataclass
class Part:
    name: str            # "Part A"
    title: str = ""      # "Multiple Choice Questions"
    questions: list = field(default_factory=list)
    lead: str = ""       # instructions for this part only
    newpage: bool = False

    @property
    def marks(self) -> int:
        return sum(q.marks or 0 for q in self.questions)


def PART(name, title="", questions=(), lead="", newpage=False) -> Part:
    return Part(name, title, list(questions), lead, newpage)


# ---- question constructors ---------------------------------------------------

def Q(text: str, marks: int, note: str = "") -> Question:
    return Question("text", marks, text=text, note=note)


def SHORT(text: str, marks: int = 1) -> Question:
    return Question("short", marks, text=text)


def MCQ(text: str, options, marks: int = 1, answer=None) -> Question:
    return Question("mcq", marks, text=text, options=tuple(options), answer=answer)


def GATEMCQ(expr, options, marks: int, answer=None, text: str = "") -> Question:
    """Read a circuit and pick its expression -- the reverse of "draw the
    circuit for this expression".

    `expr` is the boolgen expression the DRAWN circuit computes; `options` are
    boolgen expressions too (rendered in engineering notation), so every option
    on the paper comes from a real expression tree rather than hand-typed
    LaTeX. Put the direct, unsimplified reading of the circuit first: a student
    who reads the gates but never applies De Morgan's law lands on it.
    """
    return Question("mcq", marks, text=text, options=tuple(options),
                    answer=answer, payload=expr)


def SHEET(cell_range: str, marks: int, cols: int = 6, rows: int = 6,
          text: str = "") -> Question:
    """A spreadsheet grid `cols` x `rows` with `cell_range` (e.g. "B2:C3")
    shaded, asking the student to write the address of the selection.

    Column headers are letters and row headers numbers, as in Calc, so the
    student reads the address off the grid the same way they would on screen.
    """
    start, end = (_cell(r) for r in cell_range.split(":"))
    letters = [chr(ord("A") + i) for i in range(cols)]
    numbers = list(range(1, rows + 1))
    c0, c1 = sorted((letters.index(start[0]), letters.index(end[0])))
    r0, r1 = sorted((start[1], end[1]))
    assert numbers[0] <= r0 and r1 <= numbers[-1], f"{cell_range} is off the grid"
    selected = {(letters[c], r) for c in range(c0, c1 + 1)
                for r in range(r0, r1 + 1)}
    spec = SheetSpec(letters, numbers, selected, cell_range.upper())
    return Question("sheet", marks, text=text, payload=spec,
                    answer=cell_range.upper())


def CALC(headers, data, asks, marks: int, cols: int = 4, extra_rows: int = 1,
         text: str = "") -> Question:
    """A filled-in spreadsheet, and formulas whose results the student writes.

    `headers` are the column titles of row 1 and `data` the rows under them, so
    the grid is authored as the table it looks like:

        CALC(("Item", "Price"), [("Pen", 40), ("Notebook", 120)],
             asks=[("B4", "=SUM(B2:B3)")], marks=2)

    `asks` are (cell, formula) pairs; each formula is evaluated against the
    grid (calc.py) and the result kept as the setter's answer -- never printed,
    but it means a formula that the printed data cannot answer breaks the build
    instead of reaching a student. `cols` is how wide the empty sheet looks and
    `extra_rows` how many blank rows trail the data, so the grid reads like a
    real sheet with room under it rather than a table that stops dead.
    """
    letters = [chr(ord("A") + i) for i in range(cols)]
    assert len(headers) <= cols, "more headers than columns"
    values = {(letters[i], 1): h for i, h in enumerate(headers)}
    for r, row in enumerate(data, start=2):
        assert len(row) <= cols, f"row {r} is wider than the sheet"
        values.update({(letters[i], r): v for i, v in enumerate(row)})
    numbers = list(range(1, len(data) + 1 + extra_rows + 1))
    resolved = []
    for cell, f in asks:
        # the cell the formula is typed into has to be one the student can see
        # on the printed grid, or the question points off the edge of the sheet
        col, row = _cell(cell)
        assert col in letters and row in numbers, f"{cell} is off the grid"
        resolved.append((cell.upper(), f, _calc.evaluate(f, values)))
    spec = CalcSpec(letters, numbers, values, resolved)
    return Question("calc", marks, text=text, payload=spec,
                    answer=[a for _, _, a in resolved])


def TBD(marks: int, note: str = "") -> Question:
    return Question("tbd", marks, note=note)


def BOOL(expr, marks: int, ask: str, cases=(), text: str = "",
         with_table: bool = True) -> Question:
    """A Boolean-algebra question built from one boolgen expression.

    ask="truthtable"  draw the truth table (and evaluate it for `cases`)
    ask="circuit"     draw the logic-gate circuit; `with_table=False` asks for
                      the circuit alone (a short 2-mark question rather than a
                      full 4-mark one)

    `cases` are dicts like {"A": 1, "B": 0, "C": 1}: the values the student
    substitutes into the expression.
    """
    assert ask in ("truthtable", "circuit"), ask
    return Question("bool", marks, text=text, payload=expr, ask=ask,
                    cases=tuple(cases), with_table=with_table)


def TRACE(problem, marks: int, note: str = "") -> Question:
    """Trace a given flowchart, shown across the full width. `problem` is a
    flowgen TRACE problem; the student draws the trace table on the answer
    sheet, so none is printed."""
    return Question("trace", marks, payload=problem, note=note)


def DRAW(problem, marks: int, algorithm_first: bool = True,
         note: str = "") -> Question:
    """Draw the flowchart for an algorithm stated in English. `problem` is a
    flowgen DRAW problem; with `algorithm_first` the student writes the
    algorithm in words before drawing it. A flowgen `predict` list becomes a
    "trace it for these inputs" part."""
    return Question("draw", marks, payload=problem, note=note,
                    algorithm_first=algorithm_first)


def DEBUG(algo: Algorithm, bugs, cases: list, description: str, marks: int,
          note: str = "") -> Question:
    """Find the planted mistakes. `bugs` is a list of flowgen mutators; they
    are applied one after another to a copy of `algo`, so a chart can carry
    more than one logical error (flowgen's own DEBUG plants exactly one)."""
    broken = Algorithm(algo.title, copy.deepcopy(algo.body))
    for bug in bugs:
        bug(broken.body)
    assert pseudocode_lines(broken) != pseudocode_lines(algo), \
        f"the bugs did not change {algo.title!r}"
    spec = DebugSpec(algo, broken, list(cases), description, len(bugs), note)
    return Question("debug", marks, payload=spec)
