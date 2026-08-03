"""A flowchart worksheet problem.

  TRACE    given the flowchart + specific inputs -> fill the trace table
  DRAW     given the pseudocode                   -> draw the flowchart
  OUTPUTS  given the flowchart + several inputs   -> find the output for each
  DEBUG    given a flowchart with ONE mistake     -> find the box and fix it
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .algo import Algorithm
from .bug import apply_bug

KINDS = ("trace", "draw", "outputs", "debug")
PRESENTATIONS = ("flowchart", "scratch")  # how a trace/outputs problem is shown


@dataclass
class Problem:
    algo: Algorithm
    kind: str
    inputs: dict = field(default_factory=dict)
    cases: list = field(default_factory=list)  # for "outputs"/"draw" predict: input dicts
    followup: str = ""  # open-ended part (ii); answer key shows algo.title
    note: str = ""      # in-question hint (e.g. explain notation not yet taught)
    description: str = ""  # for "draw": plain-English statement instead of pseudocode
    example: str = ""   # for "draw": a worked example shown above the predict table
    reveal: str = ""    # for "trace": real-world note shown AFTER the trace table
    present: str = "flowchart"  # show the program as a flowchart, or as Scratch blocks
    bug: object = None  # for "debug": the mutation that breaks `algo` (see bug.py)
    why: str = ""       # for "debug": one-line explanation of the bug (answer key)
    broken: Algorithm | None = None  # derived: `algo` with the bug planted in it
    fix: tuple | None = None         # derived: the correction (see bug.FIXES)

    def __post_init__(self):
        assert self.kind in KINDS, f"unknown kind {self.kind!r}"
        assert self.present in PRESENTATIONS, f"unknown presentation {self.present!r}"
        if self.kind == "debug":
            assert self.bug is not None, "a debug problem needs a bug"
            assert self.cases, "a debug problem needs at least one input case"
            self.broken, self.fix = apply_bug(self.algo, self.bug)

    @property
    def shown_algo(self) -> Algorithm:
        """The program the student is shown — the buggy one for a debug problem,
        the algorithm itself otherwise."""
        return self.broken or self.algo


def TRACE(algo: Algorithm, inputs: dict, note: str = "", description: str = "",
          reveal: str = "", present: str = "flowchart") -> Problem:
    """Trace the program. `description` is an optional written use case /
    plain-English statement of the algorithm shown before it.

    `present="scratch"` shows the program as Scratch blocks instead of a
    flowchart (the student traces the Scratch script).

    `reveal` is shown AFTER the trace table — use it to name the real-world
    algorithm the flowchart implements only once the student has traced it
    (so the flowchart is presented neutrally, then explained at the end)."""
    return Problem(algo, "trace", inputs, note=note, description=description,
                   reveal=reveal, present=present)


def DRAW(algo: Algorithm, description: str = "", predict: list | None = None,
         example: str = "") -> Problem:
    """Draw the flowchart — from the derived pseudocode, or (if `description`
    is given) from a plain-English statement of the algorithm.

    If `predict` (a list of input dicts) is given, the student first works out
    by hand what the program should print for each input — so they can trace
    their own flowchart on those inputs afterwards and check it agrees. An
    optional worked `example` (prose) is shown above the predict table. The
    answer key fills the table from run(), so it can never disagree."""
    return Problem(algo, "draw", cases=predict or [], example=example,
                   description=description)


def DEBUG(algo: Algorithm, bug, cases: list, description: str,
          why: str = "", note: str = "") -> Problem:
    """Find and fix the mistake. `algo` is the CORRECT algorithm and `bug` is a
    mutator from `bug.py` (e.g. `wrong_cond("marks >= 40", "marks > 40")`); the
    flowchart shown to the student is the mutated copy.

    `description` states in plain English what the program is supposed to do —
    without it the student has nothing to check the flowchart against. For each
    input in `cases` the sheet shows what the program SHOULD print (run on
    `algo`) beside what it ACTUALLY prints (run on the buggy copy), so the
    symptom is derived, never hand-written.

    `why` is one line for the answer key explaining why the box is wrong; the
    box to change and its replacement are derived by diffing the two."""
    return Problem(algo, "debug", cases=cases, description=description,
                   bug=bug, why=why, note=note)


def OUTPUTS(algo: Algorithm, cases: list, followup: str = "", note: str = "",
            trace: dict | None = None, present: str = "flowchart") -> Problem:
    """Find the output for each input case. `trace` adds a warm-up part: trace
    the algorithm (with a trace table) for that one input first.

    `present="scratch"` shows the program as Scratch blocks instead of a
    flowchart."""
    return Problem(algo, "outputs", inputs=trace or {}, cases=cases,
                   followup=followup, note=note, present=present)
