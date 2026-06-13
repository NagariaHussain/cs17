"""A flowchart worksheet problem.

  TRACE    given the flowchart + specific inputs -> fill the trace table
  DRAW     given the pseudocode                   -> draw the flowchart
  OUTPUTS  given the flowchart + several inputs   -> find the output for each
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .algo import Algorithm

KINDS = ("trace", "draw", "outputs")


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

    def __post_init__(self):
        assert self.kind in KINDS, f"unknown kind {self.kind!r}"


def TRACE(algo: Algorithm, inputs: dict, note: str = "", description: str = "") -> Problem:
    """Trace the flowchart. `description` is an optional written use case /
    plain-English statement of the algorithm shown before the flowchart."""
    return Problem(algo, "trace", inputs, note=note, description=description)


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
            trace: dict | None = None) -> Problem:
    """Find the output for each input case. `trace` adds a warm-up part: trace
    the algorithm (with a trace table) for that one input first."""
    return Problem(algo, "outputs", inputs=trace or {}, cases=cases,
                   followup=followup, note=note)
