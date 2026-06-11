"""Seven-segment display — the single source of truth for the worksheet.

A digit is shown by lighting some of seven bars, labelled a–g and laid out:

        a
      -----
    f|     |b
     |  g  |
      -----
    e|     |c
     |     |
      -----
        d

Each digit 0–9 is authored once as the SET of segments that light up (`LIT`).
From that one fact we derive the 7 output bits (`bits`, in a,b,c,d,e,f,g order)
and the TikZ drawing of the glyph (`glyph`), so they can never disagree.
"""

from __future__ import annotations

SEGMENTS = ("a", "b", "c", "d", "e", "f", "g")

# digit -> the segments that light up (standard seven-segment numerals).
# THIS is the single source of truth; bits() and glyph() are both derived.
LIT = {
    0: "abcdef",
    1: "bc",
    2: "abdeg",
    3: "abcdg",
    4: "bcfg",
    5: "acdfg",
    6: "acdefg",
    7: "abc",
    8: "abcdefg",
    9: "abcdfg",
}


def bits(digit: int) -> list[int]:
    """The 7 output bits for `digit`, in a,b,c,d,e,f,g order (1 = lit, 0 = off)."""
    on = set(LIT[digit])
    return [1 if s in on else 0 for s in SEGMENTS]


def lit_letters(digit: int) -> list[str]:
    """The segment letters that light up for `digit`, in a–g order."""
    on = set(LIT[digit])
    return [s for s in SEGMENTS if s in on]


# the midline of each segment inside a 1×2 digit cell: (x1, y1, x2, y2)
_PATH = {
    "a": (0, 2, 1, 2),
    "b": (1, 2, 1, 1),
    "c": (1, 1, 1, 0),
    "d": (0, 0, 1, 0),
    "e": (0, 1, 0, 0),
    "f": (0, 2, 0, 1),
    "g": (0, 1, 1, 1),
}

# where to anchor each segment's label in the reference diagram
_LABEL = {
    "a": (0.5, 2.34), "b": (1.36, 1.5), "c": (1.36, 0.5), "d": (0.5, -0.34),
    "e": (-0.36, 0.5), "f": (-0.36, 1.5), "g": (0.5, 1.24),
}

_INSET = 0.17  # pull each bar back from the corners so they read as 7 bars


def _seg_draw(seg: str, color: str) -> str:
    x1, y1, x2, y2 = _PATH[seg]
    dx, dy = x2 - x1, y2 - y1
    length = (dx * dx + dy * dy) ** 0.5
    ux, uy = dx / length, dy / length
    sx, sy = x1 + ux * _INSET, y1 + uy * _INSET
    ex, ey = x2 - ux * _INSET, y2 - uy * _INSET
    return r"\draw[%s] (%.2f,%.2f) -- (%.2f,%.2f);" % (color, sx, sy, ex, ey)


def glyph(lit_segments, *, scale: float = 0.32, show_off: bool = True,
          on: str = "black", off: str = "black!10") -> str:
    """A TikZ picture of a seven-segment glyph with `lit_segments` lit. Off bars
    are drawn faintly (`show_off`) so the student sees the empty display to shade."""
    on_set = set(lit_segments)
    out = [r"\begin{tikzpicture}[scale=%g, line width=2.6pt, line cap=round, "
           r"baseline=(current bounding box.center)]" % scale]
    for seg in SEGMENTS:
        if seg in on_set:
            out.append(_seg_draw(seg, on))
        elif show_off:
            out.append(_seg_draw(seg, off))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def reference(scale: float = 1.0) -> str:
    """A labelled seven-segment diagram naming all seven bars a–g."""
    out = [r"\begin{tikzpicture}[scale=%g, line width=3pt, line cap=round]" % scale]
    for seg in SEGMENTS:
        out.append(_seg_draw(seg, "black!22"))
    for seg in SEGMENTS:
        x, y = _LABEL[seg]
        out.append(r"\node[font=\bfseries\ttfamily] at (%.2f,%.2f) {%s};" % (x, y, seg))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)
