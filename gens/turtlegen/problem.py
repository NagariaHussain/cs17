"""A coordinate / turtle worksheet problem.

  READGRID  no program; read off (or plot) labelled points on the grid
  TRACE     given a script + a blank grid -> draw the path, give the endpoint
  DRAW      given a target (a shape or a destination) -> write the script

DRAW is the primary kind: the sheet is mostly "instruct the turtle to do
something", mirroring Worksheet 10's draw-don't-trace design. The authored
program is a known-correct solution; the answer key renders it.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .program import TurtleProgram

KINDS = ("readgrid", "trace", "draw")


@dataclass
class Problem:
    kind: str
    program: TurtleProgram | None = None
    points: list = field(default_factory=list)   # readgrid: (label, x, y) to read off
    plot: list = field(default_factory=list)      # readgrid: (label, x, y) to plot
    target: str = ""        # draw/scene: plain-English statement of the goal
    show: str = "shape"     # draw: "shape" | "point" | "prose" | "dino"
    label_vertices: bool = False  # draw "shape": annotate corners with coords
    ask: str = "both"       # trace: "endpoint" | "path" | "both"
    extent: int = 6         # grid half-size for this problem
    note: str = ""          # in-question hint
    reveal: str = ""        # real-world tie-in shown AFTER the work

    def __post_init__(self):
        assert self.kind in KINDS, f"unknown kind {self.kind!r}"
        assert self.show in ("shape", "point", "prose", "dino")


def READGRID(*, points=None, plot=None, extent: int = 6, note: str = "",
             reveal: str = "") -> Problem:
    """Read off the coordinates of labelled `points`, and/or `plot` given points
    (each a (label, x, y) triple) onto the grid."""
    return Problem("readgrid", points=points or [], plot=plot or [],
                   extent=extent, note=note, reveal=reveal)


def TRACE(program: TurtleProgram, *, ask: str = "both", extent: int = 6,
          note: str = "", reveal: str = "") -> Problem:
    """Follow the script; draw the path and/or give the final position."""
    return Problem("trace", program=program, ask=ask, extent=extent,
                   note=note, reveal=reveal)


def DRAW(program: TurtleProgram, *, target: str, show: str = "shape",
         label_vertices: bool = False, extent: int = 6, note: str = "",
         reveal: str = "") -> Problem:
    """Write the turtle instructions that produce `target`. `show` chooses how
    the goal is presented: the drawn "shape" to reproduce, a single destination
    "point" to reach, "prose" only, or the "dino" mini-stage capstone."""
    return Problem("draw", program=program, target=target, show=show,
                   label_vertices=label_vertices, extent=extent, note=note,
                   reveal=reveal)
