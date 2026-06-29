"""Assemble the coordinate / turtle worksheet + answer key (two documents).

Everything is drawn inline with TikZ from the single source of truth in
`program`/`grid`, so — like segen — `build.py` just emits and compiles the .tex.
"""

from __future__ import annotations

from .. import wsbase

from . import grid
from .program import (TurtleProgram, Forward, TurnLeft, TurnRight,
                      block_label, run)
from .problem import Problem


def _uses_heading(program: TurtleProgram) -> bool:
    """Whether the program turns or moves forward — i.e. its heading matters."""
    return any(isinstance(c, (Forward, TurnLeft, TurnRight))
               for c in program.body)

_PREAMBLE = wsbase.preamble(r"""\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\newcommand{\cmd}[1]{\texttt{#1}}
\newcommand{\coordblank}{(\,\rule{1cm}{0.4pt}\,,\;\rule{1cm}{0.4pt}\,)}
""")

# heading degrees -> a word the student can picture
_HEADING_WORD = {0: "right", 90: "up", 180: "left", 270: "down"}


def _heading_word(deg: int) -> str:
    return _HEADING_WORD.get(deg % 360, "%d$^\\circ$" % (deg % 360))


_INTRO = (
    r"\textbf{The coordinate grid.}\quad Every point on the grid has two numbers: "
    r"its \emph{x} (how far across) and its \emph{y} (how far up), written "
    r"$(x, y)$. The middle, where the lines cross, is the \textbf{origin} "
    r"$(0,0)$. Right and up are positive; left and down are negative. "
    r"A \emph{turtle} sits on the grid and follows instructions to move around "
    r"and draw."
    r"\par\vspace{8pt}"
    r"\noindent\fbox{\begin{minipage}{0.96\linewidth}\small "
    r"\textbf{This is exactly how Scratch works.} The Scratch stage is one big "
    r"coordinate grid with $(0,0)$ in the middle: \emph{x} runs from $-240$ on "
    r"the far left to $240$ on the far right, and \emph{y} from $-180$ at the "
    r"bottom to $180$ at the top. The blocks \cmd{go to x:\ y:}, "
    r"\cmd{change x by}, \cmd{change y by} and \cmd{move}/\cmd{turn} move a "
    r"sprite around that grid --- the very instructions you practise below."
    r"\end{minipage}}")

# The fixed vocabulary the student writes their instructions in. (command, meaning)
_COMMANDS = [
    (r"go to x: (x)  y: (y)", "jump straight to the point $(x, y)$"),
    (r"change x by (n)",      "move across: right is $+$, left is $-$"),
    (r"change y by (n)",      "move up or down: up is $+$, down is $-$"),
    (r"move (n) steps",       "go forward in the direction you are facing"),
    (r"turn right (n) degrees", "turn clockwise (changes facing, draws nothing)"),
    (r"turn left (n) degrees",  "turn anticlockwise (changes facing, draws nothing)"),
    (r"pen up",   "lift the pen: move without drawing"),
    (r"pen down", "put the pen down: draw as you move"),
]


def _cheatsheet() -> str:
    rows = "\n".join(r"\cmd{%s} & %s \\" % (cmd, meaning)
                     for cmd, meaning in _COMMANDS)
    return (r"\textbf{Command cheat sheet.}\quad Write every answer using "
            r"\emph{only} these instructions --- they are the real Scratch "
            r"blocks. Fill the $(\,)$ slots with numbers."
            r"\par\vspace{6pt}\begin{center}\fbox{\begin{minipage}{0.96\linewidth}"
            r"\vspace{2pt}\renewcommand{\arraystretch}{1.35}"
            r"\begin{tabular}{@{}p{0.42\linewidth}@{\hspace{8pt}}l@{}}"
            + rows +
            r"\end{tabular}\vspace{2pt}\end{minipage}}\end{center}")


def _script(program: TurtleProgram) -> str:
    """The program shown as a stack of Scratch-style blocks."""
    lines = [block_label(c) for c in program.body]
    body = r"\\".join(r"\cmd{%s}" % ln for ln in lines)
    head = ""
    if program.start != (0, 0) or program.heading != 90:
        head = (r"\textit{\footnotesize Start at $(%d,%d)$ facing %s, pen down.}\\[3pt]"
                % (program.start[0], program.start[1],
                   _heading_word(program.heading)))
    return (r"\begin{center}\fbox{\begin{minipage}{0.56\linewidth}\ttfamily\small "
            + head + body + r"\end{minipage}}\end{center}")


def _write_box(n: int = 6) -> str:
    rule = r"\noindent\rule{0.82\linewidth}{0.4pt}\par\vspace{17pt}"
    return (r"\par\vspace{4pt}\textit{\footnotesize Write your instructions "
            r"here:}\par\vspace{10pt}" + rule * n)


def _side_by_side(left: str, right: str) -> str:
    return (r"\par\vspace{6pt}\begin{center}"
            r"\begin{minipage}[c]{0.46\linewidth}\centering " + left +
            r"\end{minipage}\hfill"
            r"\begin{minipage}[c]{0.5\linewidth}\centering " + right +
            r"\end{minipage}\end{center}")


def _readgrid(p: Problem, *, answer: bool) -> list[str]:
    parts = []
    if p.points:
        parts.append(r"\textbf{Read the grid.}\quad Write the coordinates "
                     r"$(x, y)$ of each labelled point.")
        parts.append(r"\par" + grid.points_grid(p.extent, p.points, reveal=answer))
        cells = []
        for label, x, y in p.points:
            ans = r"$(%d,\,%d)$" % (x, y) if answer else r"$\coordblank$"
            cells.append(r"\textbf{%s} $=$ %s" % (label, ans))
        # lay the answers out in a fixed grid so wide blanks never overflow a line
        per_row = 4
        body = r" \\[6pt] ".join(
            " & ".join(cells[i:i + per_row]) for i in range(0, len(cells), per_row))
        parts.append(r"\par\vspace{4pt}\begin{center}\begin{tabular}{%s}"
                     % ("l" * per_row) + body + r"\end{tabular}\end{center}")
    if p.plot:
        listed = ", ".join(r"\textbf{%s}$=(%d,%d)$" % (l, x, y)
                           for l, x, y in p.plot)
        parts.append(r"\textbf{Plot the points.}\quad Mark and label these "
                     r"points on the grid: " + listed + ".")
        if answer:
            parts.append(r"\par" + grid.points_grid(p.extent, p.plot, reveal=True))
        else:
            parts.append(r"\par" + grid.blank_grid(p.extent))
    if p.note:
        parts.append(r"\par\vspace{2pt}\textit{%s}" % p.note)
    if p.reveal:
        parts.append(r"\par\vspace{6pt}\textit{%s}" % p.reveal)
    return parts


def _trace(p: Problem, *, answer: bool) -> list[str]:
    result = run(p.program)
    parts = [r"\textbf{Follow the turtle.}\quad Start with the script below, "
             r"then draw the path the turtle takes and give its final position."]
    if p.note:
        parts.append(r"\par\vspace{2pt}\textit{%s}" % p.note)
    drawing = grid.path_grid(result, p.extent,
                             show_heading=_uses_heading(p.program)) if answer \
        else grid.blank_grid(p.extent)
    parts.append(_side_by_side(_script(p.program), drawing))
    if answer:
        ex, ey = result.end
        parts.append(r"\textbf{Final position:}\quad $(%d,\,%d)$\qquad"
                     r"\textbf{Now facing:}\quad %s"
                     % (ex, ey, _heading_word(result.heading)))
    else:
        parts.append(r"\par\textbf{Final position:}\quad $\coordblank$\qquad"
                     r"\textbf{Now facing:}\quad \rule{2.2cm}{0.4pt}")
    if p.reveal:
        parts.append(r"\par\vspace{6pt}\textit{%s}" % p.reveal)
    return parts


def _draw(p: Problem, *, answer: bool) -> list[str]:
    result = run(p.program)
    parts = [r"\textbf{Instruct the turtle.}\quad %s" % p.target]
    if p.note:
        parts.append(r"\par\vspace{2pt}\textit{%s}" % p.note)

    if p.show == "shape":
        target = grid.shape_grid(result, p.extent, label_vertices=p.label_vertices)
    elif p.show == "point":
        target = grid.point_target_grid(result, p.extent)
    elif p.show == "dino":
        target = grid.dino_scene(p.extent, result=result, answer=False)
    else:
        target = ""

    if target:
        parts.append(r"\par\vspace{4pt}\begin{center}" + target + r"\end{center}")

    if answer:
        parts.append(r"\textbf{One solution:}")
        parts.append(_script(p.program))
        check = grid.dino_scene(p.extent, result=result, answer=True) \
            if p.show == "dino" \
            else grid.path_grid(result, p.extent,
                                show_heading=_uses_heading(p.program))
        parts.append(r"\par\begin{center}" + check + r"\end{center}")
    else:
        parts.append(_write_box())
    if p.reveal:
        parts.append(r"\par\vspace{6pt}\textit{%s}" % p.reveal)
    return parts


def _problem_block(idx: int, p: Problem, *, answer: bool) -> str:
    parts = [r"\subsection*{Problem %d.}" % idx]
    if p.kind == "readgrid":
        parts += _readgrid(p, answer=answer)
    elif p.kind == "trace":
        parts += _trace(p, answer=answer)
    else:
        parts += _draw(p, answer=answer)
    return "\n".join(parts)


def build_document(problems, *, title: str, answer_key: bool, intro: bool = True) -> str:
    body = [_PREAMBLE, r"\begin{document}", r"\wstitle{%s}" % title]
    if answer_key:
        body.append(r"\textit{Answer key}\par\vspace{8pt}")
    else:
        body.append(r"\wsnamefield")
    if intro:
        body.append(_INTRO)
        body.append(r"\par\vspace{12pt}")
        body.append(_cheatsheet())
        body.append(r"\probrule")
    for i, p in enumerate(problems, 1):
        body.append(_problem_block(i, p, answer=answer_key))
        body.append(r"\probrule")
    body.append(r"\end{document}")
    return "\n".join(body)
