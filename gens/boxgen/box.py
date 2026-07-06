"""The Box model — one anchor point plus a width and height, the single source
of truth for every anchor-point problem.

A point on the grid is 0-dimensional: it *is* its (x, y). A sprite is not a point
— it is a box that covers a patch of the grid, and Scratch pins that box to the
grid by ONE chosen point: the box's centre. So a box has many "addresses" (its
centre, its four corners, its four edges) and Scratch reports only one of them.
This class is handed an anchor point (whichever address the author states) and
derives all the others from it, so the drawing, the worksheet and the answer key
can never disagree about where a corner sits.

Naming, kept deliberately small for beginners (Worksheet 16 uses centre + the
four corners):

    TL ────────── TR        centre  — what Scratch's (x, y) means
     │            │          BL/BR  — bottom-left / bottom-right corners
     │   centre   │          TL/TR  — top-left / top-right corners
     │            │         bottom  — the y of the lower edge (the "feet")
    BL ────────── BR            top — the y of the upper edge
"""

from __future__ import annotations

from dataclasses import dataclass

CORNERS = ("BL", "BR", "TL", "TR")
ANCHORS = ("center",) + CORNERS

# how far a corner sits from the centre, in half-widths / half-heights
_CORNER_SIGN = {"BL": (-1, -1), "BR": (1, -1), "TL": (-1, 1), "TR": (1, 1)}


def fmt(v) -> str:
    """Print a coordinate as a plain integer when it is whole (4, not 4.0)."""
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return str(v)


@dataclass
class Box:
    """A width-`w`, height-`h` box whose named point `anchor` is at (`x`, `y`).
    `anchor` is one of ANCHORS; everything else is derived from the centre."""
    anchor: str
    x: float
    y: float
    w: float
    h: float

    def __post_init__(self):
        assert self.anchor in ANCHORS, f"unknown anchor {self.anchor!r}"
        assert self.w > 0 and self.h > 0, "width and height must be positive"

    @property
    def center(self) -> tuple[float, float]:
        if self.anchor == "center":
            return (self.x, self.y)
        sx, sy = _CORNER_SIGN[self.anchor]
        # the anchor is a corner: step back to the centre by half a side
        return (self.x - sx * self.w / 2, self.y - sy * self.h / 2)

    def corner(self, name: str) -> tuple[float, float]:
        cx, cy = self.center
        sx, sy = _CORNER_SIGN[name]
        return (cx + sx * self.w / 2, cy + sy * self.h / 2)

    def point(self, name: str) -> tuple[float, float]:
        """The (x, y) of a named part: 'center' or a corner."""
        return self.center if name == "center" else self.corner(name)

    # the four edges are single coordinates (a whole edge shares one x or y)
    @property
    def bottom(self) -> float:   # y of the lower edge — the sprite's "feet"
        return self.center[1] - self.h / 2

    @property
    def top(self) -> float:
        return self.center[1] + self.h / 2

    @property
    def left(self) -> float:
        return self.center[0] - self.w / 2

    @property
    def right(self) -> float:
        return self.center[0] + self.w / 2
