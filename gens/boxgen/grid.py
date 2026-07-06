"""Draw a box on the coordinate grid, inline with TikZ.

Like turtlegen and segen there are no external figure files: every picture is a
`tikzpicture` string built straight from a `Box`, so the drawing and the stated
answer always come from the same source. The grid itself is the shared frame from
`gridframe`, identical to Worksheet 11's.
"""

from __future__ import annotations

from ..gridframe import SCALE, blank_grid, frame
from .box import Box, fmt

# where to nudge a corner's coordinate label so it sits outside the box
_CORNER_ANCHOR = {"BL": "below left", "BR": "below right",
                  "TL": "above left", "TR": "above right"}


def _dot(out, x, y, *, color, label="", place="above right", size="2.6pt"):
    out.append(r"\fill[%s] (%g,%g) circle (%s);" % (color, x, y, size))
    if label:
        out.append(r"\node[%s, font=\scriptsize] at (%g,%g) {%s};"
                   % (place, x, y, label))


def _floor(out, extent, floor):
    # label at the left end, above the line, so it never collides with the x-axis
    # arrow label when the floor happens to sit on the x-axis (floor y = 0)
    out.append(r"\draw[brown!70!black, line width=2pt] (%d,%g) -- (%d,%g);"
               % (-extent, floor, extent, floor))
    out.append(r"\node[above right, font=\tiny] at (%d,%g) {floor};"
               % (-extent, floor))


def _cactus(out, extent, floor):
    """A little obstacle resting on the floor, off to the right — sets the scene
    for the grounded-check without being part of the maths."""
    cx = extent - 2
    out.append(r"\fill[green!45!black] (%g,%g) rectangle (%g,%g);"
               % (cx - 0.4, floor, cx + 0.4, floor + 2))
    out.append(r"\node[below, font=\tiny] at (%g,%g) {cactus};" % (cx, floor))


def _rect(out, box: Box):
    (lx, by) = box.corner("BL")
    (rx, ty) = box.corner("TR")
    out.append(r"\fill[blue!8] (%g,%g) rectangle (%g,%g);" % (lx, by, rx, ty))
    out.append(r"\draw[black, very thick] (%g,%g) rectangle (%g,%g);"
               % (lx, by, rx, ty))


def _coord(name: str, x, y) -> str:
    return r"$(%s,%s)$" % (fmt(x), fmt(y))


def box_grid(box: Box, extent: int, *, outline: bool = True,
             anchor: bool = True, reveal_corners: bool = False,
             reveal_center: bool = False, floor=None, cactus: bool = False,
             scale: float = SCALE) -> str:
    """The box on the grid.

      outline         draw the rectangle (off => a blank grid to place it on)
      anchor          mark and label the box's own anchor point (what's given)
      reveal_corners  label all four corners with their (x, y) — answer key
      reveal_center   mark and label the centre — answer key
      floor / cactus  the grounded-check scene
    """
    out = frame(extent, scale)
    if floor is not None:
        _floor(out, extent, floor)
        if cactus:
            _cactus(out, extent, floor)
    if outline:
        _rect(out, box)
    if reveal_corners:
        for name in ("BL", "BR", "TL", "TR"):
            x, y = box.corner(name)
            _dot(out, x, y, color="black", size="1.8pt",
                 label=_coord(name, x, y), place=_CORNER_ANCHOR[name])
    if reveal_center or (anchor and box.anchor == "center"):
        cx, cy = box.center
        _dot(out, cx, cy, color="red!80!black",
             label=r"centre %s" % _coord("center", cx, cy))
    if anchor and box.anchor != "center":
        ax, ay = box.point(box.anchor)
        _dot(out, ax, ay, color="green!55!black",
             label=_coord(box.anchor, ax, ay), place=_CORNER_ANCHOR[box.anchor])
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def legend(scale: float = 0.7) -> str:
    """A standalone labelled box (no grid) naming the five points, for the intro:
    the centre in the middle, the four corners, and width / height braces."""
    lx, by, rx, ty = 0, 0, 6, 4
    cx, cy = 3, 2
    out = [r"\begin{tikzpicture}[scale=%g, >=Stealth]" % scale]
    out.append(r"\fill[blue!8] (%d,%d) rectangle (%d,%d);" % (lx, by, rx, ty))
    out.append(r"\draw[black, very thick] (%d,%d) rectangle (%d,%d);"
               % (lx, by, rx, ty))
    corners = {"TL": (lx, ty, "above left"), "TR": (rx, ty, "above right"),
               "BL": (lx, by, "below left"), "BR": (rx, by, "below right")}
    names = {"TL": "top-left", "TR": "top-right",
             "BL": "bottom-left", "BR": "bottom-right"}
    for key, (x, y, place) in corners.items():
        out.append(r"\fill[black] (%d,%d) circle (2pt);" % (x, y))
        out.append(r"\node[%s, font=\scriptsize] at (%d,%d) {%s};"
                   % (place, x, y, names[key]))
    out.append(r"\fill[red!80!black] (%d,%d) circle (2.6pt);" % (cx, cy))
    out.append(r"\node[above right, font=\scriptsize] at (%d,%d) {\textbf{centre}};"
               % (cx, cy))
    # width brace under the box, height brace to the left
    out.append(r"\draw[decorate, decoration={brace, amplitude=5pt, mirror}]"
               r" (%d,%.1f) -- (%d,%.1f) node[midway, below=5pt, font=\tiny]"
               r" {width};" % (lx, by - 0.4, rx, by - 0.4))
    out.append(r"\draw[decorate, decoration={brace, amplitude=5pt}]"
               r" (%.1f,%d) -- (%.1f,%d) node[midway, left=5pt, font=\tiny]"
               r" {height};" % (lx - 0.4, by, lx - 0.4, ty))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def ground_scene(*, floor_label: str, half_label: str, grounded: bool,
                 cactus: bool = True, scale: float = 0.62) -> str:
    """The capstone's schematic (no coordinate grid): the floor, the box with its
    centre marked, the drop from the centre down to the feet labelled height/2,
    and a cactus. Shows *why* the grounded test uses the feet, not the centre."""
    bw, bh = 2.2, 2.6
    by = 0.0 if grounded else 1.7          # bottom edge: on the floor, or above it
    cx = -3.0
    cy = by + bh / 2
    lx, rx = cx - bw / 2, cx + bw / 2
    out = [r"\begin{tikzpicture}[scale=%g, >=Stealth]" % scale]
    out.append(r"\draw[brown!70!black, line width=2pt] (-6.5,0) -- (6.5,0)"
               r" node[right, font=\tiny] {ground $y=%s$};" % floor_label)
    out.append(r"\fill[blue!8] (%g,%g) rectangle (%g,%g);" % (lx, by, rx, by + bh))
    out.append(r"\draw[black, very thick] (%g,%g) rectangle (%g,%g);"
               % (lx, by, rx, by + bh))
    # centre label sits above the box, clear of the cactus off to the right
    out.append(r"\fill[red!80!black] (%g,%g) circle (2.6pt);" % (cx, cy))
    out.append(r"\node[above, font=\scriptsize] at (%g,%g)"
               r" {centre \texttt{= y position}};" % (cx, by + bh))
    # the drop from the centre down to the feet: the height/2 you subtract
    out.append(r"\draw[->, gray, thick] (%g,%g) -- (%g,%g)"
               r" node[midway, left, font=\tiny] {height/2 $=%s$};"
               % (cx, cy, cx, by, half_label))
    out.append(r"\fill[green!55!black] (%g,%g) circle (2.6pt);" % (cx, by))
    out.append(r"\node[below right=1pt, font=\scriptsize] at (%g,%g) {feet};"
               % (cx, by))
    if cactus:
        ccx = 2.6
        out.append(r"\fill[green!45!black] (%g,0) rectangle (%g,1.6);"
                   % (ccx - 0.35, ccx + 0.35))
        out.append(r"\node[below, font=\tiny] at (%g,0) {cactus};" % ccx)
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)
