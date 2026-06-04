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

    def __post_init__(self):
        assert self.kind in KINDS, f"unknown kind {self.kind!r}"


def TRACE(algo: Algorithm, inputs: dict) -> Problem:
    return Problem(algo, "trace", inputs)


def DRAW(algo: Algorithm) -> Problem:
    return Problem(algo, "draw")


def OUTPUTS(algo: Algorithm, cases: list, followup: str = "") -> Problem:
    return Problem(algo, "outputs", cases=cases, followup=followup)
