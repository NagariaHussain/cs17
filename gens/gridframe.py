"""The shared coordinate-grid frame for the on-paper Scratch-prep worksheets.

turtlegen (Worksheet 11, points and the turtle) and boxgen (Worksheet 16, the
anchor point of a box) both draw the *same* grid: a light square lattice, x/y
axes with arrowheads, the origin, and even-numbered tick labels. It lives here so
the two sheets are pixel-identical and neither package owns the other's drawing.

`frame` returns the TikZ lines up to but not including `\\end{tikzpicture}`; the
caller appends its own content (a path, a box, dots) and then closes the picture.
"""

from __future__ import annotations

SCALE = 0.52


def frame(extent: int, scale: float = SCALE) -> list[str]:
    """Grid + axes + origin + even-numbered tick labels, as a list of TikZ lines.
    The caller adds content and the closing \\end{tikzpicture}."""
    e = extent
    out = [r"\begin{tikzpicture}[scale=%g, >=Stealth, line join=round, "
           r"baseline=(current bounding box.center)]" % scale]
    out.append(r"\draw[step=1, black!15, very thin] (%d,%d) grid (%d,%d);"
               % (-e, -e, e, e))
    out.append(r"\draw[->, thick] (%g,0) -- (%g,0) node[right] {$x$};"
               % (-e - 0.5, e + 0.5))
    out.append(r"\draw[->, thick] (0,%g) -- (0,%g) node[above] {$y$};"
               % (-e - 0.5, e + 0.5))
    for i in range(-e, e + 1):
        if i == 0 or i % 2:
            continue
        out.append(r"\node[below, font=\tiny] at (%d,0) {%d};" % (i, i))
        out.append(r"\node[left, font=\tiny] at (0,%d) {%d};" % (i, i))
    out.append(r"\node[below left, font=\tiny] at (0,0) {0};")
    return out


def blank_grid(extent: int, scale: float = SCALE) -> str:
    """An empty grid — what the student draws on."""
    return "\n".join(frame(extent, scale) + [r"\end{tikzpicture}"])
