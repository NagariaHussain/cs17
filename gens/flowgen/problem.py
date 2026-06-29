"""A flowchart worksheet problem.

  TRACE    given the flowchart + specific inputs -> fill the trace table
  DRAW     given the pseudocode                   -> draw the flowchart
  OUTPUTS  given the flowchart + several inputs   -> find the output for each
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .algo import Algorithm

KINDS = ("trace", "draw", "outputs")
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

    def __post_init__(self):
        assert self.kind in KINDS, f"unknown kind {self.kind!r}"
        assert self.present in PRESENTATIONS, f"unknown presentation {self.present!r}"


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


def OUTPUTS(algo: Algorithm, cases: list, followup: str = "", note: str = "",
            trace: dict | None = None, present: str = "flowchart") -> Problem:
    """Find the output for each input case. `trace` adds a warm-up part: trace
    the algorithm (with a trace table) for that one input first.

    `present="scratch"` shows the program as Scratch blocks instead of a
    flowchart."""
    return Problem(algo, "outputs", inputs=trace or {}, cases=cases,
                   followup=followup, note=note, present=present)
