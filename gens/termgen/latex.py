"""Assemble the terminal worksheet + answer key (two separate documents).

Everything renders inline - prose, ruled answer lines, write-in tables, and
verbatim terminal text - so build.py just emits the .tex and compiles it. The
only external artefact is the hand-out zip, which comes from tree.make_zip.
"""

from __future__ import annotations

import textwrap

from .. import wsbase
from . import tree as T
from .task import Task, PathTable, ErrorTable, Predict, Box, Part

_PREAMBLE = wsbase.preamble(r"""\usepackage{fancyvrb}
\usepackage{enumitem}
\usepackage{longtable}
\usepackage{array}
\setlist[enumerate]{leftmargin=*,topsep=4pt,itemsep=7pt}
\setlist[itemize]{leftmargin=*,topsep=3pt,itemsep=3pt}
\definecolor{keyrule}{HTML}{9aa3ad}
\definecolor{brand}{HTML}{888888}
% a command shown in prose: a compact grey chip. \fboxsep is trimmed so a row of
% chips stays inline-friendly, and \emergencystretch lets TeX absorb a chip that
% lands at the margin (the chips are unbreakable boxes) instead of overrunning it.
% \detokenize prints the argument literally, so author prose can write
% \cmd{IMG_0001.jpg} or \cmd{cd ~} without escaping shell punctuation by hand.
\newcommand{\cmd}[1]{{\setlength{\fboxsep}{2pt}\colorbox{gray!12}{\ttfamily\small\detokenize{#1}}}}
\setlength{\emergencystretch}{5em}
% a ruled line for a written answer (these are printed hand-outs)
\newcommand{\ansline}{\par\vspace{9pt}\noindent\textcolor{gray!70}{\rule{0.95\linewidth}{0.4pt}}}
% a part heading: number + title left, the lesson it drills right, rule under
\newcommand{\parthead}[3]{\par\vspace{6pt}%
  \noindent{\large\bfseries Part #1. #2}\hfill{\small\color{brand}#3}\par
  \vspace{3pt}{\color{gray!60}\hrule height 0.6pt}\par\vspace{9pt}}
% a boxed aside (tip / safety note / teacher note)
\newcommand{\tipbox}[2]{\par\vspace{6pt}\noindent%
  \fbox{\begin{minipage}{0.96\linewidth}\small\vspace{2pt}%
  \textbf{#1}\par\vspace{3pt}#2\vspace{2pt}\end{minipage}}\par\vspace{6pt}}
% struts that give a write-in table row room to write in
\newcommand{\wrow}{\rule[-9pt]{0pt}{30pt}}
""")

_VERB = (r"\begin{Verbatim}[fontsize=\small,xleftmargin=8pt,framesep=7pt,"
         r"frame=leftline,framerule=1.2pt,rulecolor=\color{keyrule}]")


def _esc(v) -> str:
    if v is None:
        return ""
    s = str(v)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
                 ("$", r"\$")]:
        s = s.replace(a, b)
    return s


def _tt(v) -> str:
    """A literal path or command inside a narrow table cell. Monospace fonts do
    not hyphenate, and a cell holds names like
    `photography-competition-entries-2026`, so we allow a break after every `/`
    and `-` - no hyphen is added, which would misread as part of the path."""
    s = _esc(v).replace("/", r"/\allowbreak{}").replace("-", r"-\allowbreak{}")
    return r"{\ttfamily\small %s}" % s


_VERB_COLS = 86                    # what fits in a \small verbatim at 2cm margins


def _verb(body: str, *, wrap: bool = False) -> str:
    """A verbatim block. Content is raw terminal text, so it passes through as
    typed - the only thing it may not contain is the block's own end marker.
    Verbatim does not wrap, so a long line would run off the page; `wrap` folds
    prose (the answer key's "Expected:" notes) at the column that fits. Commands
    are never wrapped, since a folded command is not one you can retype."""
    lines = []
    for line in body.rstrip("\n").split("\n"):
        if wrap and len(line) > _VERB_COLS:
            lines += textwrap.wrap(line, _VERB_COLS, break_long_words=False,
                                   break_on_hyphens=False)
        else:
            lines.append(line)
    return "\n".join([_VERB, "\n".join(lines), r"\end{Verbatim}"])


# ---- front matter ------------------------------------------------------------

def _intro(archive: T.Dir, zip_name: str, lead: str, habits: str = "",
           answer_note: str = "", answer: bool = False) -> str:
    """`lead` sets up the job, then how to get the map of the archive, then
    `habits` - the standing rules.

    The map itself is *not* printed on the worksheet. Copying it out of
    `README.txt` is the first real task of the sheet, and a map printed here
    would hand that answer over before the student has opened a terminal. The
    answer key does print it, so the teacher can check the copy."""
    parts = [lead]
    if answer_note:
        parts.append(r"\par\vspace{6pt}" + answer_note)
    parts.append(r"\par\vspace{10pt}\noindent\begin{minipage}{\linewidth}")
    parts.append(r"\textbf{What is inside \cmd{%s}.}\quad Task~1 unpacks the "
                 r"zip. You get one folder with the name \cmd{%s}, and every "
                 r"file and folder in this assignment is inside it. The map of "
                 r"that folder is not printed here. It is inside the archive, "
                 r"in \cmd{README.txt}, and Part~1 asks you to print it and "
                 r"copy it out. Keep your copy beside you: most of the work in "
                 r"this assignment is to reach the correct place in that tree."
                 % (zip_name, archive.name))
    if answer:
        # the key prints the map, so the teacher can check the student's copy.
        # \scriptsize is what keeps the whole tree on one page.
        parts.append(r"\par\vspace{6pt}")
        parts.append(r"\begin{Verbatim}[fontsize=\scriptsize,frame=single,"
                     r"framesep=8pt,rulecolor=\color{gray!55},xleftmargin=0pt]")
        parts.append(T.ascii_tree(archive))
        parts.append(r"\end{Verbatim}")
    parts.append(r"\end{minipage}")
    if habits:
        parts.append(r"\par\vspace{10pt}")
        parts.append(habits)
    return "\n".join(parts)


# ---- the write-in tables -----------------------------------------------------

def _path_table(t: PathTable, *, answer: bool) -> str:
    cols = (r"|>{\raggedright\arraybackslash}p{0.21\linewidth}"
            r"|>{\raggedright\arraybackslash}p{0.21\linewidth}"
            r"|>{\raggedright\arraybackslash}p{0.24\linewidth}"
            r"|>{\raggedright\arraybackslash}p{0.24\linewidth}|")
    head = (r"\textbf{You are in} & \textbf{You want to reach} & "
            r"\textbf{Relative path} & \textbf{Absolute path} \\")
    if not t.absolute:
        cols = (r"|>{\raggedright\arraybackslash}p{0.27\linewidth}"
                r"|>{\raggedright\arraybackslash}p{0.27\linewidth}"
                r"|>{\raggedright\arraybackslash}p{0.36\linewidth}|")
        head = (r"\textbf{You are in} & \textbf{You want to reach} & "
                r"\textbf{Command to type} \\")
    rows = []
    for row in t.rows:
        here, target, *answers = row
        cells = [_tt(here), _tt(target)]
        for a in answers:
            cells.append(_tt(a) if answer else "")
        rows.append(r"\wrow " + " & ".join(cells) + r" \\ \hline")
    cap = (r"\par\vspace{2pt}%s" % t.caption) if t.caption else ""
    return "\n".join([
        cap, r"\par\vspace{6pt}",
        r"{\small\begin{longtable}{%s}" % cols,
        r"\hline " + head + r" \hline\endhead",
        "\n".join(rows),
        r"\end{longtable}}",
    ])


def _error_table(t: ErrorTable, *, answer: bool) -> str:
    cols = (r"|>{\raggedright\arraybackslash}p{0.30\linewidth}"
            r"|>{\raggedright\arraybackslash}p{0.34\linewidth}"
            r"|>{\raggedright\arraybackslash}p{0.28\linewidth}|")
    rows = []
    for broken, err, why in t.rows:
        cells = [_tt(broken),
                 _tt(err) if answer else "",
                 (_esc(why) if answer else "")]
        rows.append(r"\wrow " + " & ".join(cells) + r" \\ \hline")
    cap = (r"\par\vspace{2pt}%s" % t.caption) if t.caption else ""
    return "\n".join([
        cap, r"\par\vspace{6pt}",
        r"{\small\begin{longtable}{%s}" % cols,
        r"\hline \textbf{Run this} & \textbf{What the shell printed} & "
        r"\textbf{Why it failed} \\ \hline\endhead",
        "\n".join(rows),
        r"\end{longtable}}",
    ])


def _predict_table(t: Predict, *, answer: bool) -> str:
    cols = (r"|>{\raggedright\arraybackslash}p{0.46\linewidth}"
            r"|>{\raggedright\arraybackslash}p{0.46\linewidth}|")
    rows = []
    for command, out in t.rows:
        rows.append(r"\wrow " + _tt(command) + " & "
                    + (_tt(out) if answer else "") + r" \\ \hline")
    cap = (r"\par\vspace{2pt}%s" % t.caption) if t.caption else ""
    return "\n".join([
        cap, r"\par\vspace{6pt}",
        r"{\small\begin{longtable}{%s}" % cols,
        r"\hline \textbf{Command} & \textbf{Write your prediction, then run the "
        r"line} \\ \hline\endhead",
        "\n".join(rows),
        r"\end{longtable}}",
    ])


def _box(b: Box, *, answer: bool) -> str:
    """A framed blank to copy something into by hand. On the key the frame
    holds the real thing instead, at the size the student sees on screen."""
    if answer:
        return "\n".join([
            b.prompt, r"\par\vspace{6pt}",
            r"\begin{Verbatim}[fontsize=\scriptsize,frame=single,framesep=8pt,"
            r"rulecolor=\color{gray!55},xleftmargin=0pt]",
            b.answer, r"\end{Verbatim}", r"\par\vspace{6pt}"])
    # \fbox of a fixed-height minipage: an empty frame the student writes in.
    # The whole thing - the instruction and the frame it refers to - goes in an
    # outer minipage, which TeX will not break: an instruction stranded at the
    # foot of one page with its box at the top of the next reads as two
    # unrelated things, and the box is large enough to trigger exactly that.
    return "\n".join([
        r"\par\vspace{4pt}\noindent\begin{minipage}{\linewidth}",
        b.prompt, r"\par\vspace{6pt}",
        r"\noindent\fbox{\begin{minipage}[t][%.2fcm][t]{0.96\linewidth}"
        r"\hspace{0pt}\end{minipage}}" % b.height,
        r"\end{minipage}\par\vspace{6pt}"])


# ---- one part ----------------------------------------------------------------

def _recap(rows: list) -> str:
    body = "\n".join(r"\cmd{%s} & %s \\" % (c, m) for c, m in rows)
    return (r"\par\vspace{2pt}\noindent\fbox{\begin{minipage}{0.96\linewidth}"
            r"\small\vspace{3pt}\textbf{Commands this part uses}"
            r"\par\vspace{4pt}\renewcommand{\arraystretch}{1.25}"
            r"\begin{tabular}{@{}l@{\hspace{12pt}}p{0.68\linewidth}@{}}"
            + body + r"\end{tabular}\vspace{3pt}\end{minipage}}\par\vspace{10pt}")


def _task_item(t: Task, *, answer: bool) -> str:
    # Instruction text is author-trusted LaTeX (it carries \cmd{...}, \emph{},
    # \texttt{} on purpose), so it passes through verbatim - same contract as
    # scratchgen's step/goal prose.
    out = [r"\item %s" % t.text]
    if t.hint:
        out.append(r"\\[2pt]{\footnotesize\itshape Hint: %s}" % t.hint)
    if t.given:
        # a command the sheet has not taught: print it on the worksheet too, so
        # the student can type it rather than guess it.
        out.append(_verb(t.given))
    if answer:
        if t.cmd:
            out.append(_verb(t.cmd))
        if t.expect:
            out.append(r"\par\vspace{-4pt}{\footnotesize\itshape\color{gray!85}"
                       r"Expected:}\vspace{-2pt}")
            out.append(_verb(t.expect, wrap=True))
    else:
        out.append(r"\ansline" * t.write)
    return "\n".join(out)


def _part(idx: int, p: Part, *, answer: bool) -> str:
    lesson = p.lesson + (r" (not taught yet)" if p.bonus else "")
    out = [r"\parthead{%d}{%s}{%s}" % (idx, _esc(p.title), _esc(lesson))]
    if p.intro:
        out.append(p.intro)
        out.append(r"\par\vspace{8pt}")
    if p.recap:
        out.append(_recap(p.recap))

    # tasks run as one numbered list; a table breaks the list and restarts it
    # after, so the numbering stays continuous down the whole part.
    open_list, n = False, 0
    for item in p.tasks:
        if isinstance(item, Task):
            if not open_list:
                out.append(r"\begin{enumerate}[resume]" if n
                           else r"\begin{enumerate}")
                open_list = True
            out.append(_task_item(item, answer=answer))
            n += 1
        else:
            if open_list:
                out.append(r"\end{enumerate}")
                open_list = False
            if isinstance(item, PathTable):
                out.append(_path_table(item, answer=answer))
            elif isinstance(item, ErrorTable):
                out.append(_error_table(item, answer=answer))
            elif isinstance(item, Predict):
                out.append(_predict_table(item, answer=answer))
            elif isinstance(item, Box):
                out.append(_box(item, answer=answer))
    if open_list:
        out.append(r"\end{enumerate}")

    if p.note:
        out.append(r"\tipbox{Remember}{%s}" % p.note)
    return "\n".join(out)


# ---- the document ------------------------------------------------------------

def build_document(parts, *, title: str, archive: T.Dir, zip_name: str,
                   lead: str, answer_key: bool, habits: str = "",
                   answer_note: str = "", reference: list | None = None,
                   closing: str = "") -> str:
    """`reference` is the end-of-sheet (command, use) recap table; `closing` is
    author LaTeX printed after the last part (the hand-in instructions)."""
    body = [_PREAMBLE, r"\begin{document}", r"\wstitle{%s}" % _esc(title)]
    if answer_key:
        body.append(r"\textit{Answer key: model commands and expected "
                    r"output. Many tasks have more than one correct answer. "
                    r"Check that the student reached the correct folder and "
                    r"the correct file.}\par\vspace{10pt}")
    else:
        body.append(r"\wsnamefield")
    body.append(_intro(archive, zip_name, lead, habits, answer_note,
                       answer=answer_key))
    body.append(r"\probrule")
    for i, p in enumerate(parts, 1):
        body.append(_part(i, p, answer=answer_key))
        body.append(r"\probrule")
    if closing:
        body.append(closing)
        body.append(r"\probrule")
    if reference:
        rows = "\n".join(r"\cmd{%s} & %s \\" % (c, u) for c, u in reference)
        body.append(r"\subsection*{Command reference}"
                    r"\par\vspace{2pt}{\small\renewcommand{\arraystretch}{1.25}"
                    r"\begin{tabular}{@{}l@{\hspace{14pt}}p{0.72\linewidth}@{}}"
                    + rows + r"\end{tabular}}")
    body.append(r"\end{document}")
    return "\n".join(body)
