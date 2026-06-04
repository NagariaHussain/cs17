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
    cases: list = field(default_factory=list)  # for "outputs": list of input dicts
    followup: str = ""  # open-ended part (ii); answer key shows algo.title
    note: str = ""      # in-question hint (e.g. explain notation not yet taught)
    description: str = ""  # for "draw": plain-English statement instead of pseudocode

    def __post_init__(self):
        assert self.kind in KINDS, f"unknown kind {self.kind!r}"


def TRACE(algo: Algorithm, inputs: dict, note: str = "", description: str = "") -> Problem:
    """Trace the flowchart. `description` is an optional written use case /
    plain-English statement of the algorithm shown before the flowchart."""
    return Problem(algo, "trace", inputs, note=note, description=description)


def DRAW(algo: Algorithm, description: str = "") -> Problem:
    """Draw the flowchart — from the derived pseudocode, or (if `description`
    is given) from a plain-English statement of the algorithm."""
    return Problem(algo, "draw", description=description)


def OUTPUTS(algo: Algorithm, cases: list, followup: str = "", note: str = "") -> Problem:
    return Problem(algo, "outputs", cases=cases, followup=followup, note=note)
