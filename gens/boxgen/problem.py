"""An anchor-point worksheet problem.

The five kinds are the sheet's ramp — read a box, place a box, compute a part,
decide above/below the floor, then write the real Scratch grounded-check block:

  NAME     a box is drawn with its centre marked; read off the (x, y) of parts
  PLACE    given an anchor point + w + h, draw the box on a blank grid
  COMPUTE  given the centre + w + h (no picture), work out a part's (x, y)
  DECIDE   given a floor line, is the box above / on / below it, and why
  GROUND   write the Scratch `if < feet < floor >` block (the capstone skill)

Everything derives from the Box, so the picture, the blanks and the key agree.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .box import Box

KINDS = ("name", "place", "compute", "decide", "ground")

# human-readable names for the parts a student reads or computes
PART_LABEL = {
    "center": "the centre",
    "BL": "the bottom-left corner",
    "BR": "the bottom-right corner",
    "TL": "the top-left corner",
    "TR": "the top-right corner",
    "bottom": "the bottom edge (the feet)",
    "top": "the top edge",
    "left": "the left edge",
    "right": "the right edge",
}
POINT_PARTS = ("center", "BL", "BR", "TL", "TR")   # answered with an (x, y)
EDGE_PARTS = ("bottom", "top", "left", "right")     # answered with one number


@dataclass
class Problem:
    kind: str
    box: Box
    parts: list = field(default_factory=list)   # name/compute: parts to read/work out
    floor: int | None = None                    # decide/ground: the ground line y
    target: str = ""                            # plain-English framing of the goal
    # ground (Scratch block) extras --------------------------------------------
    half: float = 0                 # how much to subtract off the centre (h / 2)
    relation: str = "lt"            # 'lt' or 'gt' — the comparison in the block
    negate: bool = False            # wrap the comparison in `not`
    grounded: bool = True           # draw the feet on the floor (else in the air)
    action: list = field(default_factory=list)  # scratchgen blocks inside the if
    why: str = ""                   # one-line explanation shown on the key
    # shared --------------------------------------------------------------------
    extent: int = 6
    note: str = ""
    reveal: str = ""

    def __post_init__(self):
        assert self.kind in KINDS, f"unknown kind {self.kind!r}"


def NAME(box: Box, *, parts, extent: int = 6, note: str = "",
         reveal: str = "") -> Problem:
    """The box is drawn with its centre marked and labelled; read off the (x, y)
    (or the single edge coordinate) of each part in `parts`."""
    return Problem("name", box, parts=parts, extent=extent, note=note,
                   reveal=reveal)


def PLACE(box: Box, *, target: str, extent: int = 6, note: str = "",
          reveal: str = "") -> Problem:
    """Draw `box` on a blank grid. `box.anchor` is the point the student is given;
    the answer key draws the whole box and labels its corners."""
    return Problem("place", box, target=target, extent=extent, note=note,
                   reveal=reveal)


def COMPUTE(box: Box, *, parts, target: str = "", extent: int = 6,
            note: str = "", reveal: str = "") -> Problem:
    """No picture: given the centre + w + h in prose, work out each part's (x, y).
    `box.anchor` must be 'center' — this is the pure `centre ± (w/2, h/2)` drill."""
    assert box.anchor == "center", "COMPUTE states the centre"
    return Problem("compute", box, parts=parts, target=target, extent=extent,
                   note=note, reveal=reveal)


def DECIDE(box: Box, *, floor: int, target: str, extent: int = 6, note: str = "",
           reveal: str = "") -> Problem:
    """A floor line is drawn. Is the box above / on / below it, and why? The key
    compares the box's feet (bottom edge) with the floor."""
    return Problem("decide", box, floor=floor, target=target, extent=extent,
                   note=note, reveal=reveal)


def GROUND(box: Box, *, floor: int, half: float, target: str, action,
           relation: str = "lt", negate: bool = False, grounded: bool = True,
           why: str = "", extent: int = 6, note: str = "",
           reveal: str = "") -> Problem:
    """Write the Scratch grounded-check block. A schematic scene (floor, the box
    with its feet-below-centre offset, a cactus) is drawn; the key shows the
    finished `if < (y position) - half  <  floor >` around `action`. `half` is
    h / 2. `grounded` draws the feet on the floor (else floating above it)."""
    assert relation in ("lt", "gt")
    return Problem("ground", box, floor=floor, half=half, target=target,
                   relation=relation, negate=negate, grounded=grounded,
                   action=list(action), why=why, extent=extent, note=note,
                   reveal=reveal)
