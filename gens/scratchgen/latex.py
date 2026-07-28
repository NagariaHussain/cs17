"""Assemble the build-along worksheet + answer key (two separate documents).

Everything is rendered inline (the scripts via the scratch3 package, the rest as
plain text and lists), so — like turtlegen — build.py just emits and compiles.
"""

from __future__ import annotations

from .. import wsbase

from .render import render_script
from .problem import Activity

_PREAMBLE = wsbase.preamble(r"""\usepackage{scratch3}
\usepackage{tikz}
\usetikzlibrary{arrows.meta}
\usepackage{enumitem}
\setdefaultscratch{else word=else}
% A forever loop: the package exposes \blockrepeat (a counted loop) but not the
% capped, no-bottom-nub forever block; build it from the internal C-block macro
% scr_blockloop{text}{body}{else}{infinite}{arrow} with infinite + arrow on.
\newcommand\blockforever[1]{\csname scr_blockloop\endcsname{forever}{#1}{}11}
% repeat until <cond>: the package ships \blockrepeat (counted) but no public
% repeat-until, so build it from the same internal C-block macro — a finite loop
% (no infinite flag, no loop arrow) whose header carries the boolean hexagon.
\newcommand\blockrepeatuntil[2]{\csname scr_blockloop\endcsname{repeat until #1}{#2}{}00}
% counted repeat: the bundled \blockrepeat draws the count oval but omits the word
% "repeat", so build our own from the internal C-block macro — a finite loop WITH
% the loop arrow (infinite off, arrow on) whose header reads "repeat (n)".
\newcommand\blockrepeatn[2]{\csname scr_blockloop\endcsname{repeat #1}{#2}{}01}
% a "your turn" gap: a grey stack block the student must replace with the real
% block. It reuses the package's own block primitive \scr_normalblock{colour}{text}
% (the same one \blockmove etc. call) so it stacks with correct puzzle nubs; only
% the colour is ours. scr_normalblock uses colour "dd" for its outline, so both
% scrgap and scrgapdd are defined. (\scr_normalblock has an underscore, not a
% letter in this document, so it is reached via \csname, like \blockforever above.)
\definecolor{scrgap}{HTML}{8a8a8a}
\definecolor{scrgapdd}{HTML}{5f5f5f}
\newcommand\blockgap[1]{\csname scr_normalblock\endcsname{scrgap}{\textbf{?}\ \textit{your turn:} #1}}
% A "your turn" gap for the test of an if / repeat-until: a grey hexagon so the
% if SHELL still shows while only its boolean is left blank. \scr_boolbox{colour}
% {text} is the package's own hexagon primitive (\booloperator etc. call it),
% reached via \csname because of the underscore.
\newcommand\boolgap[1]{\csname scr_boolbox\endcsname{scrgap}{\textbf{?}\ #1}}
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

# every block group the generator can show, in canonical Scratch order, named so
# the student can find each block fast. The colour names match the official
# Scratch 3.0 palette. A worksheet shows only the subset it uses (PALETTE in its
# module); DEFAULT_PALETTE is Scratch A's basic set.
_PALETTE = [
    ("Motion",    "blue",        "Move the sprite: move, turn, go to, point towards, change x or y."),
    ("Looks",     "purple",      "Change how the sprite looks: say, costume, size, backdrop."),
    ("Sound",     "pink",        "Play a sound."),
    ("Events",    "yellow",      "Start a script (green flag, key, click, when I receive) and broadcast messages."),
    ("Control",   "orange",      "Choose when and how often blocks run: wait, forever, repeat, if, stop."),
    ("Sensing",   "light blue",  "Ask about the world: touching?, key pressed?, mouse, ask and answer."),
    ("Operators", "green",       "Do maths and comparisons: plus, pick random, less-than, equals, more-than, and/or."),
    ("Variables", "dark orange", "Remember a value like score: set, change, and show a variable."),
]
DEFAULT_PALETTE = ["Motion", "Looks", "Sound", "Events", "Control"]


def _palette(names: list | None = None) -> str:
    names = names or DEFAULT_PALETTE
    rows = "\n".join(
        r"\textbf{%s} & \textit{(%s)} & %s \\" % (name, colour, _esc(desc))
        for name, colour, desc in _PALETTE if name in names)
    return (r"\textbf{The block groups you will use.}\quad Each block has a "
            r"colour. The colour tells you which group it is in. Find the colour "
            r"first, then find the block."
            r"\par\vspace{6pt}\begin{center}\fbox{\begin{minipage}{0.96\linewidth}"
            r"\vspace{2pt}\renewcommand{\arraystretch}{1.3}"
            r"\begin{tabular}{@{}l l p{0.62\linewidth}@{}}"
            + rows +
            r"\end{tabular}\vspace{2pt}\end{minipage}}\end{center}")


# ---- one activity ------------------------------------------------------------

def _scripts_block(scripts, answer: bool = False, stack: bool = False) -> str:
    """The finished script(s), centred. A lone script (or a `stack`ed set) sits
    full width, one per row; otherwise several are laid two to a row (so a
    four-arrow project wraps instead of overrunning the page), each with its
    caption underneath. On the answer key (`answer=True`) any gaps render filled
    in; on the worksheet they show as "your turn" placeholders. `stack` forces
    the full-width one-per-row layout even for several scripts - use it when a
    script holds a wide block (a long gap hint) that a half-width column clips."""
    full = len(scripts) == 1 or stack
    scale = 0.85 if full else 0.7
    width = r"\linewidth" if full else r"\dimexpr 0.48\linewidth-4pt"
    cells = []
    for s in scripts:
        cap = (r"\\[3pt]\footnotesize\itshape %s" % _esc(s.caption)) if s.caption else ""
        cells.append(r"\begin{minipage}[t]{%s}\centering %s%s\end{minipage}"
                     % (width, render_script(s, scale=scale, answer=answer), cap))
    if full:
        rows = cells                                   # each script on its own row
    else:
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
        parts.append(_scripts_block(a.scripts, answer=answer, stack=a.stack))

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
                   intro: bool = True, palette: list | None = None,
                   lead: str | None = None) -> str:
    """`palette` is the list of block-group names to show in the colour key
    (defaults to Scratch A's basic set). `lead` replaces the first-time "What is
    Scratch?" tour with a short recap for later sheets; the colour key still shows."""
    body = [_PREAMBLE, r"\begin{document}", r"\wstitle{%s}" % title]
    if answer_key:
        body.append(r"\textit{Answer key --- finished scripts and challenge "
                    r"solutions.}\par\vspace{8pt}")
    else:
        body.append(r"\wsnamefield")
    if intro:
        body.append(lead if lead else _INTRO)
        body.append(r"\par\vspace{12pt}")
        body.append(_palette(palette))
        body.append(r"\probrule")
    for i, a in enumerate(activities, 1):
        body.append(_activity(i, a, answer=answer_key))
        body.append(r"\probrule")
    body.append(r"\end{document}")
    return "\n".join(body)
