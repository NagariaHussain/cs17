"""Draw the coordinate grid and turtle paths inline with TikZ.

Like segen, these are pure functions returning a `tikzpicture` string — there are
no external figure files. Every drawing is built from a `TraceResult` (or a list
of points), so the picture and the stated answer come from the same source.
"""

from __future__ import annotations

from ..gridframe import SCALE, blank_grid, frame as _frame
from .program import TraceResult


def _start_marker(out: list[str], x, y):
    out.append(r"\fill[green!55!black] (%g,%g) circle (2.4pt);" % (x, y))
    out.append(r"\node[below left, font=\scriptsize] at (%g,%g) {start};" % (x, y))


def path_grid(result: TraceResult, extent: int, scale: float = SCALE, *,
              show_heading: bool = True) -> str:
    """The full traced path: solid arrows for pen-down moves, dashed for pen-up
    jumps, a marker for the start (with its initial heading) and the endpoint.
    `show_heading` draws the initial-facing arrow — only meaningful when the
    program actually turns/moves (not for change-x/change-y-only programs)."""
    out = _frame(extent, scale)
    sx, sy = result.start
    if show_heading:
        out.append(r"\draw[->, orange!85!black, thick] (%g,%g) -- +(%d:0.9);"
                   % (sx, sy, result.start_heading))
    for x1, y1, x2, y2, pen in result.segments:
        if pen:
            out.append(r"\draw[blue, very thick, ->] (%g,%g) -- (%g,%g);"
                       % (x1, y1, x2, y2))
        else:
            out.append(r"\draw[gray, dashed, thick] (%g,%g) -- (%g,%g);"
                       % (x1, y1, x2, y2))
    _start_marker(out, sx, sy)
    ex, ey = result.end
    out.append(r"\fill[red!80!black] (%g,%g) circle (2.6pt);" % (ex, ey))
    out.append(r"\node[above right, font=\scriptsize] at (%g,%g) {$(%d,%d)$};"
               % (ex, ey, ex, ey))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def shape_grid(result: TraceResult, extent: int, scale: float = SCALE, *,
               label_vertices: bool = False) -> str:
    """The drawn outline only (pen-down segments), as a target to reproduce —
    no direction arrows. Optionally annotate each corner with its coordinates."""
    out = _frame(extent, scale)
    for x1, y1, x2, y2, pen in result.segments:
        if pen:
            out.append(r"\draw[black, very thick] (%g,%g) -- (%g,%g);"
                       % (x1, y1, x2, y2))
    _start_marker(out, *result.start)
    if label_vertices:
        seen = set()
        for vx, vy in result.visited:
            if (vx, vy) in seen:
                continue
            seen.add((vx, vy))
            out.append(r"\fill[black] (%g,%g) circle (1.6pt);" % (vx, vy))
            out.append(r"\node[above right, font=\tiny] at (%g,%g) {$(%d,%d)$};"
                       % (vx, vy, vx, vy))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def point_target_grid(result: TraceResult, extent: int, scale: float = SCALE) -> str:
    """Just the start and the destination dot (with its coordinates) — no route.
    Used when the task is to work out the moves that reach a marked point."""
    out = _frame(extent, scale)
    _start_marker(out, *result.start)
    ex, ey = result.end
    out.append(r"\fill[red!80!black] (%g,%g) circle (2.8pt);" % (ex, ey))
    out.append(r"\node[above right, font=\scriptsize] at (%g,%g) "
               r"{target $(%d,%d)$};" % (ex, ey, ex, ey))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def points_grid(extent: int, points, *, reveal: bool, scale: float = SCALE) -> str:
    """Labelled dots. On the worksheet (reveal=False) only the letters show; on
    the answer key (reveal=True) each dot also carries its (x, y)."""
    out = _frame(extent, scale)
    for label, x, y in points:
        out.append(r"\fill[blue!70!black] (%g,%g) circle (2.6pt);" % (x, y))
        if reveal:
            out.append(r"\node[above right, font=\scriptsize] at (%g,%g) "
                       r"{\textbf{%s}\,$(%d,%d)$};" % (x, y, label, x, y))
        else:
            out.append(r"\node[above right, font=\scriptsize] at (%g,%g) "
                       r"{\textbf{%s}};" % (x, y, label))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)


def dino_scene(extent: int, scale: float = SCALE, *, result: TraceResult | None,
               answer: bool) -> str:
    """The capstone mini-stage: a floor line, the dino, and a cactus sliding in
    from the right. On the answer key the dino's jump (the program's path) is
    drawn as the up-and-down arc."""
    floor = -4
    out = _frame(extent, scale)
    # the ground
    out.append(r"\draw[brown!70!black, line width=2pt] (%d,%d) -- (%d,%d);"
               % (-extent, floor, extent, floor))
    # the dino, resting on the floor
    dx, dy = result.start if result else (-6, floor)
    out.append(r"\fill[green!55!black] (%g,%g) circle (3pt);" % (dx, dy))
    out.append(r"\node[below, font=\scriptsize] at (%g,%g) {Dino};" % (dx, dy))
    # a cactus to the right, two squares tall, with a "slides left" arrow
    cx = -2
    out.append(r"\fill[green!45!black] (%g,%g) rectangle (%g,%g);"
               % (cx - 0.25, floor, cx + 0.25, floor + 2))
    out.append(r"\node[below, font=\scriptsize] at (%g,%g) {cactus};" % (cx, floor))
    out.append(r"\draw[->, gray, thick] (%g,%g) -- (%g,%g) "
               r"node[midway, above, font=\tiny] {slides left};"
               % (cx - 0.7, floor + 2.6, cx - 2.2, floor + 2.6))
    if answer and result:
        for x1, y1, x2, y2, pen in result.segments:
            out.append(r"\draw[blue, very thick, ->] (%g,%g) -- (%g,%g);"
                       % (x1, y1, x2, y2))
    out.append(r"\end{tikzpicture}")
    return "\n".join(out)
