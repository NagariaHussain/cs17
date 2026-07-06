"""Assemble the anchor-point worksheet + answer key (two documents).

Everything is inline: the grids and the box are TikZ (see `grid`), and the
capstone's grounded-check is drawn with the scratch3 package by reusing
scratchgen's renderer, so the block the student writes is the very block the key
shows. Like the other cs17 generators, `build.py` just emits and compiles.
"""

from __future__ import annotations

from .. import wsbase
from ..scratchgen.render import render_blocks
from ..scratchgen.script import gt, if_, lt, not_, sub, y_position
from . import grid
from .box import fmt
from .problem import EDGE_PARTS, PART_LABEL, Problem

_PREAMBLE = wsbase.preamble(r"""\usepackage{tikz}
\usetikzlibrary{arrows.meta, decorations.pathreplacing}
\usepackage{scratch3}
\newcommand{\cmd}[1]{\texttt{#1}}
\newcommand{\coordblank}{(\,\rule{1cm}{0.4pt}\,,\;\rule{1cm}{0.4pt}\,)}
\newcommand{\blk}[1]{{\setlength{\fboxsep}{2pt}\colorbox{gray!12}{\ttfamily\small #1}}}
""")

_INTRO = (
    r"\textbf{A point is a spot. A sprite is a box.}\quad "
    r"A point has two numbers: its \emph{x} (how far across) and its \emph{y} "
    r"(how far up), written $(x, y)$. But a sprite in Scratch is not a single "
    r"spot. It is a \emph{box} that covers a patch of the grid. So how does "
    r"Scratch know where the box sits? It pins the box to the grid by "
    r"\emph{one} point: the \textbf{centre}. When Scratch says a sprite is at "
    r"$(x, y)$, it means the \emph{centre} of the box is at $(x, y)$."
    r"\par\vspace{6pt}"
    r"The box has other important points too. It has four \textbf{corners} and "
    r"four \textbf{edges}. Each one has its own coordinates."
    r"\par\vspace{8pt}\begin{center}" + grid.legend() + r"\end{center}"
    r"\par\vspace{4pt}"
    r"\textbf{Finding a corner from the centre.}\quad A corner is half a width "
    r"across and half a height up or down from the centre. So:"
    r"\par\vspace{4pt}\begin{center}"
    r"corner $x$ = centre $x \;\pm\;$ (width $\div\, 2$)\qquad\qquad "
    r"corner $y$ = centre $y \;\pm\;$ (height $\div\, 2$)"
    r"\end{center}"
    r"\par\vspace{4pt}"
    r"\noindent\fbox{\begin{minipage}{0.96\linewidth}\small "
    r"\textbf{Why this matters for the Dino game.} To check if the Dino is "
    r"standing on the ground, you must look at its \emph{feet}: the bottom "
    r"edge. You cannot look at the centre, because the centre sits higher up. "
    r"The feet are at (centre $y$) minus (height $\div\, 2$). Scratch only "
    r"tells you the centre with \cmd{y position}, so you subtract half the "
    r"height yourself. Get this wrong and the Dino floats above the floor or "
    r"sinks into it."
    r"\end{minipage}}")


def _part_row(box, part, *, answer: bool) -> tuple[str, str]:
    """A (label, answer) pair for one part read off or worked out."""
    if part in EDGE_PARTS:
        axis = "y" if part in ("bottom", "top") else "x"
        val = getattr(box, part)
        ans = (r"$%s = %s$" % (axis, fmt(val))) if answer \
            else (r"$%s = \rule{1.8cm}{0.4pt}$" % axis)
    else:
        x, y = box.point(part)
        ans = (r"$(%s,\,%s)$" % (fmt(x), fmt(y))) if answer else r"$\coordblank$"
    return (PART_LABEL[part], ans)


def _parts_table(box, parts, *, answer: bool) -> str:
    rows = "\n".join(
        r"%s & %s \\[4pt]" % _part_row(box, p, answer=answer) for p in parts)
    return (r"\par\vspace{4pt}\begin{center}"
            r"\begin{tabular}{@{}p{0.55\linewidth}@{\hspace{10pt}}l@{}}"
            + rows + r"\end{tabular}\end{center}")


def _dims(box) -> str:
    return r"It is \textbf{%s} wide and \textbf{%s} tall." % (fmt(box.w), fmt(box.h))


def _note(parts, s) -> None:
    if s:
        parts.append(r"\par\vspace{2pt}\textit{%s}" % s)


def _reveal(parts, s) -> None:
    if s:
        parts.append(r"\par\vspace{6pt}\textit{%s}" % s)


def _name(p: Problem, *, answer: bool) -> list[str]:
    parts = [r"\textbf{Read the box.}\quad The box below has its centre marked. "
             r"%s Write the coordinates of each part." % _dims(p.box)]
    _note(parts, p.note)
    fig = grid.box_grid(p.box, p.extent, anchor=True, reveal_center=True,
                        reveal_corners=answer)
    parts.append(r"\par\vspace{4pt}\begin{center}" + fig + r"\end{center}")
    parts.append(_parts_table(p.box, p.parts, answer=answer))
    _reveal(parts, p.reveal)
    return parts


def _place(p: Problem, *, answer: bool) -> list[str]:
    parts = [r"\textbf{Place the box.}\quad %s" % p.target]
    _note(parts, p.note)
    if answer:
        fig = grid.box_grid(p.box, p.extent, anchor=True, outline=True,
                            reveal_corners=True, reveal_center=True)
    else:
        # the given anchor dot only, on an otherwise blank grid to draw on
        fig = grid.box_grid(p.box, p.extent, anchor=True, outline=False)
    parts.append(r"\par\vspace{4pt}\begin{center}" + fig + r"\end{center}")
    _reveal(parts, p.reveal)
    return parts


def _compute(p: Problem, *, answer: bool) -> list[str]:
    cx, cy = p.box.center
    lead = p.target or (
        r"A box has its centre at $(%s,%s)$. %s There is no picture this time. "
        r"Work out the coordinates using the rule above."
        % (fmt(cx), fmt(cy), _dims(p.box)))
    parts = [r"\textbf{Work it out.}\quad " + lead]
    _note(parts, p.note)
    parts.append(_parts_table(p.box, p.parts, answer=answer))
    _reveal(parts, p.reveal)
    return parts


def _status(box, floor) -> str:
    feet = box.bottom
    if feet > floor:
        return "above the floor"
    if feet == floor:
        return "resting on the floor"
    return "below the floor (sunk in)"


def _decide(p: Problem, *, answer: bool) -> list[str]:
    parts = [r"\textbf{Above or below?}\quad %s" % p.target]
    _note(parts, p.note)
    fig = grid.box_grid(p.box, p.extent, anchor=True, reveal_center=True,
                        reveal_corners=answer, floor=p.floor)
    parts.append(r"\par\vspace{4pt}\begin{center}" + fig + r"\end{center}")
    if answer:
        feet = p.box.bottom
        cy = p.box.center[1]
        parts.append(
            r"\textbf{Answer:} the box is \textbf{%s}.\par\vspace{2pt}"
            r"The feet are at centre $y$ minus height$\,\div 2 = %s - %s = %s$. "
            r"The floor is at $%s$. Since $%s$ is %s $%s$, the box is %s."
            % (_status(p.box, p.floor), fmt(cy), fmt(p.box.h / 2), fmt(feet),
               fmt(p.floor), fmt(feet),
               _rel_word(feet, p.floor), fmt(p.floor), _status(p.box, p.floor)))
    else:
        parts.append(r"\par Circle one:\quad \textbf{above} \quad / \quad "
                     r"\textbf{on} \quad / \quad \textbf{below} the floor."
                     r"\par\vspace{8pt}\textit{\footnotesize Then show your "
                     r"working: the feet are at $y = \rule{2.2cm}{0.4pt}$, the "
                     r"floor is at $y = \rule{2cm}{0.4pt}$.}")
    _reveal(parts, p.reveal)
    return parts


def _rel_word(a, b) -> str:
    return "greater than" if a > b else ("equal to" if a == b else "less than")


def _ground_cond(p: Problem):
    """The boolean the student must write: (y position) - half  </>  floor."""
    feet = sub(y_position(), p.half)
    cond = lt(feet, p.floor) if p.relation == "lt" else gt(feet, p.floor)
    return not_(cond) if p.negate else cond


def _if_block(cond, action, scale: float = 0.95) -> str:
    return render_blocks([if_(cond, *action)], scale=scale)


def _ground(p: Problem, *, answer: bool) -> list[str]:
    parts = [r"\textbf{Write the block.}\quad %s" % p.target]
    _note(parts, p.note)
    scene = grid.ground_scene(floor_label=fmt(p.floor), half_label=fmt(p.half),
                              grounded=p.grounded)
    parts.append(r"\par\vspace{4pt}\begin{center}" + scene + r"\end{center}")
    if answer:
        parts.append(r"\textbf{The block:}")
        parts.append(r"\par\vspace{2pt}\begin{center}"
                     + _if_block(_ground_cond(p), p.action) + r"\end{center}")
        if p.why:
            parts.append(r"\par\vspace{2pt}\textit{%s}" % p.why)
    else:
        # the block skeleton with an EMPTY hexagon for the student to fill in,
        # plus a line to write the condition out in text
        parts.append(r"\par\vspace{2pt}\textit{\footnotesize Fill in the empty "
                     r"hexagon with the \cmd{if} condition:}")
        parts.append(r"\par\vspace{4pt}\begin{center}"
                     + _if_block(r"\boolempty[11em]", p.action) + r"\end{center}")
        parts.append(r"\par\vspace{2pt}\textit{\footnotesize Or write it here:}"
                     r"\par\vspace{6pt}\noindent\rule{0.82\linewidth}{0.4pt}"
                     r"\par\vspace{10pt}")
    _reveal(parts, p.reveal)
    return parts


_RENDER = {"name": _name, "place": _place, "compute": _compute,
           "decide": _decide, "ground": _ground}


def _problem_block(idx: int, p: Problem, *, answer: bool) -> str:
    parts = [r"\subsection*{Problem %d.}" % idx]
    parts += _RENDER[p.kind](p, answer=answer)
    return "\n".join(parts)


def build_document(problems, *, title: str, answer_key: bool,
                   intro: bool = True) -> str:
    body = [_PREAMBLE, r"\begin{document}", r"\wstitle{%s}" % title]
    if answer_key:
        body.append(r"\textit{Answer key}\par\vspace{8pt}")
    else:
        body.append(r"\wsnamefield")
    if intro:
        body.append(_INTRO)
        body.append(r"\probrule")
    for i, p in enumerate(problems, 1):
        body.append(_problem_block(i, p, answer=answer_key))
        body.append(r"\probrule")
    body.append(r"\end{document}")
    return "\n".join(body)
