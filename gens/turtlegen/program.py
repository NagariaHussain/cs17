"""Turtle program model — the single source of truth for a coordinate problem.

A program is authored once as a small list of movement commands. From it we
derive both the drawing (-> grid.py, the TikZ path) and the ground-truth answer
(-> run(), below: the endpoint, the final heading, and every segment drawn), so
the worksheet and the answer key can never disagree.

Coordinates are a Cartesian grid centred on (0, 0): x runs across, y runs up.
Heading is in degrees, measured the maths way: 0 = facing right (+x),
90 = facing up (+y); `turn left` adds to the heading (anticlockwise), `turn
right` subtracts. The turtle starts facing up (heading 90), matching the
"point upwards" intuition. Turns are authored in multiples of 90 degrees so a
`move` always lands on an integer lattice point the student can read off by hand.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


# ---- commands ----------------------------------------------------------------

@dataclass
class Forward:
    n: int          # steps along the current heading (negative = backwards)


@dataclass
class TurnLeft:
    deg: int


@dataclass
class TurnRight:
    deg: int


@dataclass
class GoTo:
    x: int
    y: int


@dataclass
class ChangeX:
    n: int


@dataclass
class ChangeY:
    n: int


@dataclass
class PenUp:
    pass


@dataclass
class PenDown:
    pass


@dataclass
class Home:
    pass


# tiny constructors so worksheets read like a stack of Scratch blocks
def fd(n: int) -> Forward:
    return Forward(n)


def bk(n: int) -> Forward:
    return Forward(-n)


def lt(deg: int) -> TurnLeft:
    return TurnLeft(deg)


def rt(deg: int) -> TurnRight:
    return TurnRight(deg)


def goto(x: int, y: int) -> GoTo:
    return GoTo(x, y)


def changex(n: int) -> ChangeX:
    return ChangeX(n)


def changey(n: int) -> ChangeY:
    return ChangeY(n)


def penup() -> PenUp:
    return PenUp()


def pendown() -> PenDown:
    return PenDown()


def home() -> Home:
    return Home()


@dataclass
class TurtleProgram:
    title: str
    body: list
    start: tuple = (0, 0)
    heading: int = 90       # 90 = facing up (+y)


# ---- block labels (the Scratch block each command maps to) -------------------

def block_label(cmd) -> str:
    """The Scratch motion/pen block this command corresponds to, shown verbatim
    on the sheet so the printed script and the executed script can never drift."""
    if isinstance(cmd, Forward):
        return "move %d steps" % cmd.n
    if isinstance(cmd, TurnLeft):
        return "turn left %d degrees" % cmd.deg
    if isinstance(cmd, TurnRight):
        return "turn right %d degrees" % cmd.deg
    if isinstance(cmd, GoTo):
        return "go to x: %d  y: %d" % (cmd.x, cmd.y)
    if isinstance(cmd, ChangeX):
        return "change x by %d" % cmd.n
    if isinstance(cmd, ChangeY):
        return "change y by %d" % cmd.n
    if isinstance(cmd, PenUp):
        return "pen up"
    if isinstance(cmd, PenDown):
        return "pen down"
    if isinstance(cmd, Home):
        return "go to x: 0  y: 0"
    raise AssertionError(cmd)


# ---- the interpreter (execute to the ground-truth answer) --------------------

@dataclass
class TraceResult:
    start: tuple
    start_heading: int
    end: tuple
    heading: int
    segments: list = field(default_factory=list)  # (x1, y1, x2, y2, pen_down)
    visited: list = field(default_factory=list)    # ordered points, incl. jumps


def run(prog: TurtleProgram) -> TraceResult:
    """Execute the turtle program and return its full geometry."""
    x, y = prog.start
    heading = prog.heading
    pen = True
    segments: list = []
    visited = [(x, y)]

    def move_to(nx, ny):
        nonlocal x, y
        segments.append((x, y, nx, ny, pen))
        x, y = nx, ny
        visited.append((x, y))

    for cmd in prog.body:
        if isinstance(cmd, Forward):
            rad = math.radians(heading)
            move_to(x + round(cmd.n * math.cos(rad)),
                    y + round(cmd.n * math.sin(rad)))
        elif isinstance(cmd, TurnLeft):
            heading = (heading + cmd.deg) % 360
        elif isinstance(cmd, TurnRight):
            heading = (heading - cmd.deg) % 360
        elif isinstance(cmd, GoTo):
            move_to(cmd.x, cmd.y)
        elif isinstance(cmd, ChangeX):
            move_to(x + cmd.n, y)
        elif isinstance(cmd, ChangeY):
            move_to(x, y + cmd.n)
        elif isinstance(cmd, PenUp):
            pen = False
        elif isinstance(cmd, PenDown):
            pen = True
        elif isinstance(cmd, Home):
            heading = 90
            move_to(0, 0)
        else:
            raise AssertionError(cmd)

    return TraceResult(start=prog.start, start_heading=prog.heading,
                       end=(x, y), heading=heading,
                       segments=segments, visited=visited)
