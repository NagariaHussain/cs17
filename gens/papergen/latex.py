"""Assemble the question paper + answer key (two separate documents).

Everything renders inline — the spreadsheet grids as tabulars, the Scratch
solution scripts via scratchgen's own renderer — so build.py just emits and
compiles, the way turtlegen and scratchgen do.

Reuse, not reimplement: the scratch3 macro setup comes from
`scratchgen.latex.SCRATCH_EXTRA` and the block rendering from
`scratchgen.render_script`, so a Scratch answer on a paper is drawn by exactly
the code that draws the Scratch worksheets.
"""

from __future__ import annotations

from .. import wsbase
from ..scratchgen.latex import SCRATCH_EXTRA
from ..scratchgen.render import render_script

from .paper import Paper, Section, Question, Part, SheetTable

_PREAMBLE = wsbase.preamble(SCRATCH_EXTRA + r"""
% - exam chrome -------------------------------------------------------------
% The duration / maximum-marks bar that sits under the title, and the marks tag
% that closes each part's heading line (\hfill pushes it to the right margin).
\newcommand{\paperinfo}[2]{%
  \noindent\textbf{Time:}~#1\hfill\textbf{Maximum Marks:}~#2%
  \par\vspace{4pt}{\color{gray!60}\hrule height 0.4pt}\par\vspace{14pt}}
\newcommand{\qmarks}[1]{\hfill\textnormal{\bfseries[#1]}}
% a section banner: the section name in a light band across the text width
\newcommand{\sectionband}[1]{%
  \par\vspace{6pt}\noindent\colorbox{gray!15}{%
    \begin{minipage}{\dimexpr\linewidth-2\fboxsep}%
      \vspace{2pt}\centering\bfseries #1\vspace{2pt}%
    \end{minipage}}\par\vspace{12pt}}
% the "- End of Section X -" / end-of-paper centred rule line
\newcommand{\closingline}[1]{%
  \par\vspace{10pt}\begin{center}\textit{\textcolor{gray}{- #1 -}}\end{center}
  \par\vspace{4pt}}
% spreadsheet grids: a light rule colour so the data reads before the gridlines,
% and a shaded strip for the column letters / row numbers, as a real sheet shows.
\usepackage{array}
\definecolor{gridline}{HTML}{BBBBBB}
\newcommand{\sheetname}[1]{{\ttfamily\small #1}}
""")

# the column-letter strip and row-number gutter, styled like a spreadsheet frame
_HEADSTRIP = r"\cellcolor{gray!25}"
_GUTTER = r">{\columncolor{gray!25}}c"


# Applied in ONE pass (see _esc): replacing sequentially would re-escape the
# braces of an already-substituted replacement, so a source backslash would come
# out as \textbackslash\{\} — a backslash followed by two literal braces.
_ESCAPES = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "$": r"\$",
}


def _esc(v) -> str:
    """Escape a data value. Prose fields are author-trusted and bypass this."""
    if v is None:
        return ""
    return "".join(_ESCAPES.get(ch, ch) for ch in str(v))


def fx(s: str) -> str:
    """A spreadsheet formula or cell reference set as code. Formulas are dense
    with LaTeX specials ($ absolute refs, _ in sheet names), so authoring writes
    them literally and this escapes them."""
    return r"\texttt{%s}" % _esc(s)


# ---- spreadsheet grids --------------------------------------------------------

def _sheet_table(t: SheetTable) -> str:
    """One table drawn as a spreadsheet: lettered columns, numbered rows, and
    shaded empty cells for the columns the student must fill with formulas."""
    # Column widths come from the author (the second half of each heading pair is
    # a (text, width) tuple when a width is given); default to a snug p-column.
    specs, heads = [], []
    for letter, head in t.columns:
        if isinstance(head, tuple):
            text, width = head
        else:
            text, width = head, "1.6cm"
        specs.append(r">{\centering\arraybackslash}p{%s}" % width)
        heads.append((letter, text))

    colspec = "|" + _GUTTER + "|" + "|".join(specs) + "|"
    lines = [r"\begin{center}",
             r"\arrayrulecolor{gridline}\renewcommand{\arraystretch}{1.25}",
             # a nine-column sales register overruns the text block at the default
             # column padding, so the grids run tight and small
             r"\setlength{\tabcolsep}{4pt}\footnotesize",
             r"\begin{tabular}{%s}" % colspec,
             r"\hline"]

    # the A / B / C … strip
    letter_cells = " & ".join(r"%s\textbf{%s}" % (_HEADSTRIP, letter)
                              for letter, _ in heads)
    lines.append(r"\cellcolor{gray!25} & %s \\ \hline" % letter_cells)

    # row 1 — the sheet's own header row
    head_cells = " & ".join(r"\textbf{%s}" % _esc(text) for _, text in heads)
    lines.append(r"\textbf{1} & %s \\ \hline" % head_cells)

    # the data rows, numbered from 2
    for n, row in enumerate(t.rows, 2):
        cells = []
        for (letter, _), value in zip(heads, row):
            if t.is_blank(letter):
                cells.append(r"\cellcolor{gray!7}")
            else:
                cells.append(_esc(value))
        lines.append(r"\textbf{%d} & %s \\ \hline" % (n, " & ".join(cells)))

    lines += [r"\end{tabular}", r"\arrayrulecolor{black}", r"\end{center}"]

    out = []
    if t.new_page:
        out.append(r"\clearpage")
    out.append(r"\par\vspace{4pt}\noindent\textbf{Sheet:}~\sheetname{%s}" % _esc(t.sheet))
    if t.note:
        out.append(r"\par\vspace{2pt}{\small\itshape %s}" % t.note)
    out.append("\n".join(lines))
    return "\n".join(out)


# ---- questions ----------------------------------------------------------------

def _items(items, roman: bool = True) -> str:
    """The (i)/(ii)/(iii) sub-instructions of a part."""
    if not items:
        return ""
    style = "label=(\\roman*)" if roman else "label=(\\alph*)"
    body = "\n".join(r"\item %s" % s for s in items)
    return (r"\begin{enumerate}[%s,leftmargin=2.2em,topsep=3pt,itemsep=3pt]" % style
            + body + r"\end{enumerate}")


def _scripts_block(scripts, answer: bool = True, scale: float | None = None) -> str:
    """Scratch scripts, two to a row, each captioned — scratchgen's own renderer,
    so these are the same blocks the Scratch worksheets draw. `answer=False` is
    for a script the student is *given* (any gap stays an unfilled placeholder)."""
    if not scripts:
        return ""
    full = len(scripts) == 1
    scale = scale if scale else (0.8 if full else 0.62)
    width = r"\linewidth" if full else r"\dimexpr 0.48\linewidth-4pt"
    cells = []
    for s in scripts:
        cap = (r"\\[3pt]\footnotesize\itshape %s" % _esc(s.caption)) if s.caption else ""
        cells.append(r"\begin{minipage}[t]{%s}\centering %s%s\end{minipage}"
                     % (width, render_script(s, scale=scale, answer=answer), cap))
    rows = cells if full else [r"\hfill".join(cells[i:i + 2])
                               for i in range(0, len(cells), 2)]
    return (r"\par\vspace{8pt}\begin{center}"
            + r"\par\vspace{14pt}".join(rows) + r"\end{center}")


def _part(q: Question, p: Part, *, answer_key: bool) -> str:
    head = r"%d %s" % (q.number, p.label)
    if p.title:
        head += r"\quad %s" % _esc(p.title)
    out = [r"\par\vspace{10pt}\noindent\textbf{%s}\qmarks{%s}\par\vspace{4pt}"
           % (head, _marklabel(p.marks))]
    if p.text:
        out.append(p.text)
    if p.given:
        out.append(_scripts_block(p.given, answer=False))
    if p.items:
        out.append(_items(p.items))
    if p.note:
        out.append(r"\par\vspace{3pt}{\itshape %s\par}" % p.note)

    if answer_key:
        body = []
        if p.answer:
            body.append(p.answer)
        if p.answer_items:
            body.append(_items(p.answer_items))
        if body:
            out.append(r"\par\vspace{5pt}\noindent\textbf{\textcolor{gray!80}"
                       r"{Answer.}}\par\vspace{3pt}")
            out += body
        if p.scripts:
            out.append(_scripts_block(p.scripts))
        if p.answer_note:
            out.append(r"\par\vspace{4pt}{\itshape %s\par}" % p.answer_note)
    return "\n".join(out)


def _marklabel(n: int) -> str:
    return f"{n} mark" if n == 1 else f"{n} marks"


def _question(q: Question, *, answer_key: bool) -> str:
    head = r"Question %d" % q.number
    if q.title:
        head += r" - %s" % _esc(q.title)
    out = [r"\par\vspace{6pt}\noindent{\large\bfseries %s}\qmarks{%s}"
           r"\par\vspace{3pt}{\color{gray!60}\hrule height 0.4pt}\par\vspace{8pt}"
           % (head, _marklabel(q.marks))]
    if q.intro:
        out.append(q.intro)
    if q.given:
        # a given script is reference material the student reads while answering
        # every part, so it runs slightly tighter than a full-page solution
        out.append(_scripts_block(q.given, answer=False, scale=0.6))
    for p in q.parts:
        out.append(_part(q, p, answer_key=answer_key))
    return "\n".join(out)


def _section(s: Section, *, answer_key: bool) -> str:
    # A single-section hand-out has nothing to distinguish itself FROM, so an
    # unnamed section drops the band (and its end marker) and just runs its
    # questions — the question heading already carries the marks.
    out = []
    if s.new_page:
        out.append(r"\clearpage")
    if s.name:
        band = s.name if not s.title else r"%s - %s" % (s.name, _esc(s.title))
        out.append(r"\sectionband{%s\hfill %s}" % (band, _marklabel(s.marks)))
    if s.scenario:
        out.append(r"\noindent\textbf{Scenario}\par\vspace{3pt}")
        out.append(s.scenario)
    for t in s.tables:
        out.append(_sheet_table(t))
    for q in s.questions:
        out.append(_question(q, answer_key=answer_key))
    if s.outro:
        out.append(r"\par\vspace{6pt}{\itshape %s\par}" % s.outro)
    if s.name:
        out.append(r"\closingline{End of %s}" % _esc(s.name))
    return "\n".join(out)


# ---- the instructions box -----------------------------------------------------

def _instructions(items) -> str:
    body = "\n".join(r"\item %s" % s for s in items)
    return (r"\noindent\fbox{\begin{minipage}{\dimexpr\linewidth-2\fboxsep-2\fboxrule}"
            r"\small\vspace{3pt}\textbf{General Instructions}"
            r"\begin{enumerate}[leftmargin=2em,topsep=3pt,itemsep=2pt]"
            + body +
            r"\end{enumerate}\vspace{3pt}\end{minipage}}\par\vspace{16pt}")


# ---- assembly -----------------------------------------------------------------

def build_document(paper: Paper, *, answer_key: bool) -> str:
    paper.check()
    body = [_PREAMBLE, r"\begin{document}", r"\wstitle{%s}" % _esc(paper.title)]

    if answer_key:
        body.append(r"\textit{Answer key and marking scheme - not for "
                    r"distribution.}\par\vspace{8pt}")
    else:
        body.append(r"\wsnamefield")

    body.append(r"\paperinfo{%s}{%d}" % (_esc(paper.duration), paper.marks))

    if paper.instructions and not answer_key:
        body.append(_instructions(paper.instructions))

    for s in paper.sections:
        body.append(_section(s, answer_key=answer_key))

    if paper.footer_note and not answer_key:
        body.append(r"{\itshape %s\par}" % paper.footer_note)
    body.append(r"\closingline{End of Question Paper}")
    body.append(r"\end{document}")
    return "\n".join(body)
