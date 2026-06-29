"""turtlegen — coordinate-grid / turtle-instructions practice-sheet generator.

Author each turtle program once; derive both the drawing and the ground-truth
answer (endpoint, heading, path) from the same source so they can never disagree.
The instruction vocabulary maps 1:1 to Scratch motion + pen blocks, priming the
stage coordinate system before students open Scratch.
"""

from .program import (
    TurtleProgram, run, block_label,
    fd, bk, lt, rt, goto, changex, changey, penup, pendown, home,
)
from .problem import Problem, READGRID, TRACE, DRAW

__all__ = [
    "TurtleProgram", "run", "block_label",
    "fd", "bk", "lt", "rt", "goto", "changex", "changey", "penup", "pendown",
    "home", "Problem", "READGRID", "TRACE", "DRAW",
]
