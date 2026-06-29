"""Assemble the build-along worksheet + answer key (two separate documents).

Everything is rendered inline (the scripts via the scratch3 package, the rest as
plain text and lists), so — like turtlegen — build.py just emits and compiles.
"""

from __future__ import annotations

from .. import wsbase

from .render import render_script
from .problem import Activity

_PREAMBLE = wsbase.preamble(r"""\usepackage{scratch3}
\usepackage{enumitem}
\setdefaultscratch{else word=else}
% A forever loop: the package exposes \blockrepeat (a counted loop) but not the
% capped, no-bottom-nub forever block; build it from the internal C-block macro
% scr_blockloop{text}{body}{else}{infinite}{arrow} with infinite + arrow on.
\newcommand\blockforever[1]{\csname scr_blockloop\endcsname{forever}{#1}{}11}
% a block name in prose: a compact grey chip. \fboxsep is trimmed so a row of
% several chips stays inline-friendly, and \emergencystretch lets TeX absorb a
% chip that lands at the margin (the chips are unbreakable boxes) instead of
% overrunning it.
\newcommand{\blk}[1]{{\setlength{\fboxsep}{2pt}\colorbox{gray!12}{\ttfamily\small #1}}}
\setlength{\emergencystretch}{5em}
\setlist[enumerate]{leftmargin=*,topsep=3pt,itemsep=3pt}
\setlist[itemize]{leftmargin=*,topsep=3pt,itemsep=3pt}
""")


def _esc(v) -> str:
    if v is None:
        return ""
    s = str(v)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}")]:
        s = s.replace(a, b)
    return s


# ---- the front matter: a tour of the Scratch screen, then a colour key -------

_INTRO = (
    r"\textbf{What is Scratch?}\quad Scratch lets you build programs by snapping "
    r"coloured \emph{blocks} together, like jigsaw pieces. You do not type any "
    r"code. You drag a block into the \emph{code area}, then join blocks under "
    r"each other to make a \emph{script}. When you click the green flag, your "
    r"script runs from the top block down to the bottom block. To start, open "
    r"\texttt{scratch.mit.edu} and click \emph{Create}."
    r"\par\vspace{8pt}"
    r"\noindent\fbox{\begin{minipage}{0.96\linewidth}\small\vspace{2pt}"
    r"\textbf{The screen has four main parts.}\par\vspace{3pt}"
    r"\begin{itemize}"
    r"\item The \textbf{stage} (top right) is where your \emph{sprite} (the cat) "
    r"moves and your project plays.\\"
    r"\item The \textbf{sprite list} (under the stage) shows every character. "
    r"Click one to give it code.\\"
    r"\item The \textbf{block list} (middle) holds all the blocks, sorted by "
    r"colour.\\"
    r"\item The \textbf{code area} (right) is where you join blocks together."
    r"\end{itemize}\vspace{2pt}\end{minipage}}")

# the colour groups this sheet uses, named so the student can find each block
# fast. The colours match the official Scratch 3.0 category palette.
_PALETTE = [
    ("Motion",  "blue",   "Move the sprite: move, turn, go to, point, change x or y."),
    ("Looks",   "purple", "Change how the sprite looks: say, costume, size."),
    ("Sound",   "pink",   "Play a sound."),
    ("Events",  "yellow", "Hat blocks that start a script: green flag, key pressed, sprite clicked."),
    ("Control", "orange", "Choose when and how often blocks run: wait, forever, repeat."),
]


def _palette() -> str:
    rows = "\n".join(
        r"\textbf{%s} & \textit{(%s)} & %s \\" % (name, colour, _esc(desc))
        for name, colour, desc in _PALETTE)
    return (r"\textbf{The block groups you will use.}\quad Each block has a "
            r"colour. The colour tells you which group it is in. Find the colour "
            r"first, then find the block."
            r"\par\vspace{6pt}\begin{center}\fbox{\begin{minipage}{0.96\linewidth}"
            r"\vspace{2pt}\renewcommand{\arraystretch}{1.3}"
            r"\begin{tabular}{@{}l l p{0.62\linewidth}@{}}"
            + rows +
            r"\end{tabular}\vspace{2pt}\end{minipage}}\end{center}")


# ---- one activity ------------------------------------------------------------

def _scripts_block(scripts) -> str:
    """The finished script(s), centred. One sits full width; several are laid two
    to a row (so a four-arrow project wraps instead of overrunning the page),
    each with its caption underneath."""
    one = len(scripts) == 1
    scale = 0.85 if one else 0.7
    width = r"\linewidth" if one else r"\dimexpr 0.48\linewidth-4pt"
    cells = []
    for s in scripts:
        cap = (r"\\[3pt]\footnotesize\itshape %s" % _esc(s.caption)) if s.caption else ""
        cells.append(r"\begin{minipage}[t]{%s}\centering %s%s\end{minipage}"
                     % (width, render_script(s, scale=scale), cap))
    rows = [r"\hfill".join(cells[i:i + 2]) for i in range(0, len(cells), 2)]
    return (r"\par\vspace{6pt}\begin{center}"
            + r"\par\vspace{12pt}".join(rows) + r"\end{center}")


def _activity(idx: int, a: Activity, *, answer: bool) -> str:
    # The prose fields (goal, steps, challenges, ...) are author-trusted LaTeX —
    # they carry \blk{...}, \emph{}, $+$, \% on purpose — so they pass through
    # verbatim, exactly as turtlegen treats its note/target/reveal text.
    parts = [r"\subsection*{Project %d: %s}" % (idx, _esc(a.title))]
    parts.append(r"\textit{%s}" % a.goal)

    if a.setup:
        parts.append(r"\par\vspace{4pt}\textbf{Get ready.}\quad %s" % a.setup)

    if a.new_blocks:
        rows = "\n".join(r"\blk{%s} & %s \\" % (b, m) for b, m in a.new_blocks)
        parts.append(r"\par\vspace{4pt}\textbf{New blocks.}"
                     r"\par\vspace{3pt}\begin{center}"
                     r"\begin{tabular}{@{}l@{\hspace{10pt}}p{0.6\linewidth}@{}}"
                     + rows + r"\end{tabular}\end{center}")

    if a.steps:
        parts.append(r"\par\vspace{2pt}\textbf{Build it.}")
        items = "\n".join(r"\item %s" % s for s in a.steps)
        parts.append(r"\begin{enumerate}" + items + r"\end{enumerate}")

    if a.scripts:
        if a.script_intro:
            parts.append(r"\par\vspace{2pt}%s" % a.script_intro)
        parts.append(_scripts_block(a.scripts))

    if a.note:
        parts.append(r"\par\vspace{2pt}\textit{%s}" % a.note)

    if a.tasks:
        parts.append(r"\par\vspace{4pt}\textbf{Your task.}\quad Now make your "
                     r"project better. Do these in order. Each one builds on the "
                     r"last.")
        items = []
        for instruction, result in a.tasks:
            item = r"\item %s" % instruction
            if answer and result:
                item += r"\\[1pt]\textit{\textcolor{gray!75}{Expected: %s}}" % result
            items.append(item)
        parts.append(r"\begin{enumerate}" + "\n".join(items) + r"\end{enumerate}")

    return "\n".join(parts)


def build_document(activities, *, title: str, answer_key: bool,
                   intro: bool = True) -> str:
    body = [_PREAMBLE, r"\begin{document}", r"\wstitle{%s}" % title]
    if answer_key:
        body.append(r"\textit{Answer key --- finished scripts and challenge "
                    r"solutions.}\par\vspace{8pt}")
    else:
        body.append(r"\wsnamefield")
    if intro:
        body.append(_INTRO)
        body.append(r"\par\vspace{12pt}")
        body.append(_palette())
        body.append(r"\probrule")
    for i, a in enumerate(activities, 1):
        body.append(_activity(i, a, answer=answer_key))
        body.append(r"\probrule")
    body.append(r"\end{document}")
    return "\n".join(body)
