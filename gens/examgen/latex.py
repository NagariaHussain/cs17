"""LaTeX for an exam question paper.

A paper is authored as a module holding the header fields (title, subject,
paper, duration, maximum marks) and a list PARTS of `question.PART(...)`.
Questions are numbered continuously across the parts. An empty PARTS list
renders as the title block alone (the boilerplate to fill in).

Flowchart questions delegate to flowgen's own renderers (trace tables, the
draw-here box, the should-print/actually-prints table) and Boolean questions to
boolgen's expression renderer, so an exam question looks exactly like the
worksheet questions the students practised on — same source, same output.

Students answer on a separate answer sheet, so the paper carries NO writing
space: no ruled lines, no draw-here boxes, no blank tables. Every question is
the question and the material it needs (a flowchart, an expression, the
symptom table of a buggy chart) and nothing else.

No answer key: an exam paper ships on its own.
"""

from __future__ import annotations

from .. import wsbase
from ..boolgen.expr import Gate, Var
from ..boolgen.latex import expr_latex
from ..flowgen import latex as _flow
from ..flowgen.algo import pseudocode_lines, run

_EXTRA = r"""
\usepackage{enumitem}
\usepackage{amsmath}
\usepackage{amssymb}   % \checkmark, used in the "tick the correct option" lead
\usepackage{array}
\usepackage{needspace}
% marks flush right on the question's first line
\newcommand{\qmarks}[1]{\hfill\textnormal{\small[#1]}}
% part heading: name + title left, the part's marks right, thin rule under
\newcommand{\parthead}[2]{%
  \par\vspace{4pt}\Needspace*{4\baselineskip}%
  {\large\bfseries #1}\hfill{\small\itshape #2}\par
  \vspace{3pt}{\color{gray!60}\hrule height 0.6pt}\par\vspace{10pt}}
"""

PREAMBLE = wsbase.preamble(_EXTRA)


# ---- header ------------------------------------------------------------------

def _field(label: str, value: str) -> str:
    return rf"\textbf{{{label}:}}~{value}"


def _header(*, title, subject, paper, duration, max_marks=None, date=None) -> str:
    """Title rule, then the fields in two columns, then the Name-Date blanks.

    Fields are laid out left-to-right in pairs so the block stays compact and
    the second column lines up with the Date blank underneath it.
    """
    fields = [_field("Subject", subject)]
    if paper:
        fields.append(_field("Paper", paper))
    fields.append(_field("Time allowed", duration))
    if max_marks is not None:
        fields.append(_field("Maximum marks", str(max_marks)))
    if date:  # sits under "Time allowed" -- see the pairing below
        fields.append(_field("Date", date))

    pairs = [fields[i:i + 2] for i in range(0, len(fields), 2)]
    rows = [" & ".join(p + [""] * (2 - len(p))) for p in pairs]
    # Name / Date share the same two columns, so the blanks line up with the
    # fields above them instead of drifting to the page margins. When the paper
    # prints its own exam date there is nothing for the student to date, so the
    # Name blank takes the full width.
    rows.append(r"\multicolumn{2}{@{}l@{}}{Name:~\hrulefill}" if date
                else r"Name:~\hrulefill & Date:~\hrulefill")

    return "\n".join([
        rf"\wstitle{{{title}}}",
        r"\begin{tabular}{@{}p{0.58\textwidth}p{0.37\textwidth}@{}}",
        (" \\\\[5pt]\n").join(rows[:-1]) + " \\\\[22pt]\n" + rows[-1],
        r"\end{tabular}",
        r"\par\vspace{14pt}{\color{black}\hrule height 0.4pt}\par\vspace{18pt}",
    ])


def _instructions(items) -> str:
    if not items:
        return ""
    lines = [r"\textbf{Instructions}",
             r"\begin{itemize}[leftmargin=*,itemsep=2pt,topsep=4pt]"]
    lines += [rf"  \item {it}" for it in items]
    lines += [r"\end{itemize}", r"\vspace{14pt}"]
    return "\n".join(lines)


# ---- small pieces ------------------------------------------------------------

def _stem(num: int, text: str, marks) -> str:
    tail = rf"\qmarks{{{marks}}}" if marks is not None else ""
    return rf"\textbf{{Q{num}.}}~{text}{tail}\par\vspace{{4pt}}"


def _sub(label: str, text: str) -> str:
    return rf"\par\vspace{{6pt}}\textbf{{({label})}}~{text}\par"


def _values(case: dict) -> str:
    return ", ".join(f"${k} = {v}$" for k, v in case.items())


def _prose(text: str) -> str:
    """A question's description, with maths left alone.

    flowgen's `_esc` escapes backslashes, so a description written entirely
    through it can never carry a formula. Here anything between a pair of $ is
    passed to LaTeX untouched and everything outside is escaped as usual, so a
    statement can say $1 \\times 2 \\times \\cdots \\times n$ and have it set as
    maths instead of spelling it out in ASCII."""
    return "$".join(part if i % 2 else _flow._esc(part)
                    for i, part in enumerate(text.split("$")))


# ---- one question ------------------------------------------------------------

def _option(opt) -> str:
    """An option is either plain text or a boolgen expression."""
    if isinstance(opt, (Var, Gate)):
        return r"$Y = %s$" % expr_latex(opt)
    return opt


def _mcq(num, q, fig_path="") -> str:
    parts = [_needspace(q), _stem(num, q.text, q.marks)]
    if fig_path:  # a GATEMCQ: the circuit is the question
        parts.append(r"\par\vspace{2pt}\begin{center}"
                     r"\includegraphics[max width=0.55\linewidth,"
                     r"max totalheight=0.22\textheight]{%s}\end{center}" % fig_path)
    parts.append(r"\begin{enumerate}[label=(\alph*),leftmargin=*,itemsep=3pt,topsep=2pt]")
    parts += [rf"  \item {_option(opt)}" for opt in q.options]
    parts.append(r"\end{enumerate}")
    return "\n".join(parts)


def _bool(num, q) -> str:
    """A Boolean question: the expression, then what to do with it.

    With sub-parts the stem only introduces the expression -- the work is
    stated once, in (i) and (ii). Saying "draw the truth table" in the stem AND
    again in (i) reads as two different demands. A question with no sub-parts
    (a circuit on its own) carries the whole instruction in the stem instead."""
    e = q.payload
    ask = q.ask
    subparts = ask == "truthtable" or q.with_table
    if subparts:
        default = "For the Boolean expression below:"
    else:
        default = "Draw the logic-gate circuit for the Boolean expression below."
    parts = [_stem(num, q.text or default, q.marks),
             r"\[ Y = %s \]" % expr_latex(e)]
    if ask == "truthtable":
        parts.append(_sub("i", "Draw the complete truth table for $Y$."))
        if q.cases:
            asked = " and when ".join(_values(c) for c in q.cases)
            parts.append(_sub("ii", "Find the value of $Y$ when %s. "
                                    "Show the substitution." % asked))
    elif q.with_table:
        parts.append(_sub("i", "Draw the logic-gate circuit for $Y$."))
        parts.append(_sub("ii", "Draw the truth table for the same circuit."))
    return "\n".join(parts)


def _fig(fig_path) -> str:
    """A flowchart, as big as the page allows.

    Note `width=` (not `max width=`): graphviz's natural size is small and
    adjustbox's max-constraints only ever shrink, so a chart has to be scaled UP
    to the text width first; the height cap then pulls back a tall one."""
    return (r"\par\vspace{6pt}\begin{center}"
            r"\includegraphics[width=\linewidth,"
            r"max totalheight=0.6\textheight]{%s}\end{center}" % fig_path)


# how much of a page a question's block needs in one piece; the part heading
# reserves the same amount for its first question, so a heading is never left
# stranded at the foot of a page while its question jumps to the next one
_NEED = {"trace": 0.8, "debug": 0.8, "draw": 0.25, "mcq": 0.2,
         "sheet": 0.3}


def _needspace(q) -> str:
    frac = _NEED.get(q.kind)
    if q.kind == "mcq" and q.payload is not None:  # a GATEMCQ carries a circuit
        frac = 0.45
    return r"\Needspace*{%s\textheight}" % frac if frac else ""


def _trace(num, q, fig_path) -> str:
    p = q.payload
    # the table is a TEMPLATE, not answer space: the right columns (run() names
    # them) and two blank rows, for the student to copy onto the answer sheet.
    cols, rows, _ = run(p.algo, p.inputs)
    parts = [_needspace(q)]
    text = _flow._trace_instruction(p.inputs, "algorithm",
                                    closing="and draw the trace table")
    parts.append(_stem(num, text, q.marks))
    if p.description:
        parts.append(r"\begin{quote}\itshape %s\end{quote}" % _prose(p.description))
    if p.note or q.note:
        parts.append(r"\par\textit{%s}" % _flow._esc(p.note or q.note))
    parts.append(_fig(fig_path))
    parts.append(r"\par\vspace{2pt}\begin{center}"
                 r"\textcolor{gray!70}{\footnotesize\itshape Copy this table "
                 r"into your answer sheet and complete it.}\par\vspace{5pt}"
                 + _flow._trace_table(cols, rows, fill=False, n_rows=2)
                 + r"\end{center}")
    return "\n".join(parts)


def _draw(num, q) -> str:
    p = q.payload
    parts = [_needspace(q), _stem(num, q.text or _DRAW_STEM, q.marks)]
    if p.description:
        parts.append(r"\begin{quote}\itshape %s\end{quote}" % _prose(p.description))
    if q.note:
        parts.append(r"\par\textit{%s}" % _flow._esc(q.note))
    labels = iter(["i", "ii", "iii"])
    if q.algorithm_first:
        parts.append(_sub(next(labels), "Write the algorithm in words, step by step."))
    parts.append(_sub(next(labels), "Draw the flowchart for that algorithm."))
    if p.cases:
        # the inputs are named in the prompt rather than laid out as a blank
        # table -- the student's trace goes on the answer sheet
        asked = " and ".join(_case_text(c) for c in p.cases)
        parts.append(_sub(next(labels), "Trace your flowchart for %s, and write "
                                        "what it prints in each case." % asked))
    return "\n".join(parts)


def _case_text(case: dict) -> str:
    return ", ".join(f"${k} = {v}$" for k, v in case.items())


_DRAW_STEM = "Read the description below, then answer the parts that follow."


def _debug(num, q, fig_path) -> str:
    spec = q.payload
    # the number of mistakes is NOT given away -- finding out how many there are
    # is part of the question
    stem = (r"The flowchart below is \textbf{meant} to do what the italic line "
            r"says, but there are mistakes in it. The table under the flowchart "
            r"shows what it should print and what it actually prints. "
            r"\textbf{Find all the mistakes in this flowchart, then draw the "
            r"corrected flowchart in your answer sheet}, so that it gives the "
            r"correct expected output.")
    # a short chart (no loop, a handful of boxes) blown up to 0.62 of the page
    # is all whitespace and giant boxes, so the cap follows the box count
    boxes = len(pseudocode_lines(spec.broken))
    height = "0.62" if boxes > 6 else "0.3"
    parts = [_needspace(q), _stem(num, stem, q.marks),
             r"\begin{quote}\itshape %s\end{quote}" % _prose(spec.description)]
    if spec.note:
        parts.append(r"\par\textit{%s}" % _flow._esc(spec.note))
    parts += [
        r"\par\vspace{6pt}\begin{center}",
        # scaled to a readable height first (see _fig), then capped in width so
        # a chart with a wide loop still fits the text block
        r"\includegraphics[totalheight=%s\textheight,"
        r"max width=\linewidth]{%s}" % (height, fig_path),
        r"\par\vspace{10pt}",
        _flow._symptom_table(spec),
        r"\end{center}",
    ]
    return "\n".join(parts)


def _sheet(num, q) -> str:
    """A spreadsheet as the student sees it in Calc: lettered column headers,
    numbered row headers, and the selected block shaded."""
    g = q.payload
    stem = q.text or (r"The shaded cells in the spreadsheet below are selected. "
                      r"Write the address of this selection.")
    head_cell = r"\cellcolor{gray!25}"
    col = r">{\centering\arraybackslash}p{1.1cm}"
    parts = [_stem(num, stem, q.marks),
             r"\par\vspace{4pt}\begin{center}",
             r"\begin{tabular}{|c|%s}" % ("|".join([col] * len(g.cols)) + "|"),
             r"\hline",
             " & ".join([head_cell] + [head_cell + r"\textbf{%s}" % c
                                       for c in g.cols]) + r" \\ \hline"]
    for r in g.rows:
        cells = [head_cell + r"\textbf{%d}" % r]
        cells += [(r"\cellcolor{blue!20}" if (c, r) in g.selected else "")
                  + r"\rule{0pt}{3.2ex}" for c in g.cols]
        parts.append(" & ".join(cells) + r" \\ \hline")
    parts += [r"\end{tabular}", r"\end{center}"]
    return "\n".join(parts)


def _calc(num, q) -> str:
    """A sheet with data in it, then one sub-part per formula.

    The grid is drawn the way Calc shows it (lettered columns, numbered rows,
    the data left in the cells) so the student reads the addresses off the
    picture; the formulas sit underneath in typewriter type, as they would in
    the input line."""
    g = q.payload
    stem = q.text or (r"The spreadsheet below is open in LibreOffice Calc. "
                      r"Write what appears in each cell after the formula is "
                      r"typed into it and Enter is pressed.")
    head_cell = r"\cellcolor{gray!25}"
    wide = r">{\raggedright\arraybackslash}p{2.4cm}"
    narrow = r">{\centering\arraybackslash}p{1.6cm}"
    body = [wide] + [narrow] * (len(g.cols) - 1)
    parts = [_needspace(q), _stem(num, stem, q.marks),
             r"\par\vspace{4pt}\begin{center}",
             r"\begin{tabular}{|c|%s}" % ("|".join(body) + "|"),
             r"\hline",
             " & ".join([head_cell] + [head_cell + r"\textbf{%s}" % c
                                       for c in g.cols]) + r" \\ \hline"]
    for r in g.rows:
        cells = [head_cell + r"\textbf{%d}" % r]
        for c in g.cols:
            v = g.values.get((c, r), "")
            body_text = r"\textbf{%s}" % _flow._esc(v) if r == 1 and v != "" \
                else _flow._esc(v)
            cells.append(r"\rule{0pt}{3.2ex}" + body_text)
        parts.append(" & ".join(cells) + r" \\ \hline")
    parts += [r"\end{tabular}", r"\end{center}"]
    for label, (cell, formula, _) in zip(["i", "ii", "iii", "iv"], g.asks):
        parts.append(_sub(label, r"Cell %s holds the formula \texttt{%s}. "
                                 r"What does %s show?"
                          % (cell, _flow._esc(formula), cell)))
    return "\n".join(parts)


def _plain(num, q) -> str:
    text = q.text
    if q.kind == "tbd":
        text = r"\textit{TBD}" + (rf" --- {q.note}" if q.note else "")
    parts = [_stem(num, text, q.marks)]
    if q.note and q.kind != "tbd":
        parts.append(r"\par\textit{%s}" % q.note)
    return "\n".join(p for p in parts if p)


def _question(num: int, q, fig_path: str) -> str:
    if q.kind == "mcq":
        return _mcq(num, q, fig_path)
    if q.kind == "bool":
        return _bool(num, q)
    if q.kind == "trace":
        return _trace(num, q, fig_path)
    if q.kind == "draw":
        return _draw(num, q)
    if q.kind == "debug":
        return _debug(num, q, fig_path)
    if q.kind == "sheet":
        return _sheet(num, q)
    if q.kind == "calc":
        return _calc(num, q)
    return _plain(num, q)


# ---- the paper ---------------------------------------------------------------

def _part_head(part) -> str:
    name = part.name + (f" --- {part.title}" if part.title else "")
    # keep the heading with its first question
    lead = _needspace(part.questions[0]) if part.questions else ""
    n = len(part.questions)
    tally = f"{n} question{'s' if n != 1 else ''} --- {part.marks} marks"
    return lead + r"\parthead{%s}{%s}" % (name, tally)


def build_document(parts, *, title, subject, paper, duration,
                   max_marks=None, instructions=(), figs=None, date=None) -> str:
    """parts: list of question.Part. figs: {question index (1-based): path}."""
    figs = figs or {}
    body = [
        PREAMBLE,
        r"\begin{document}",
        _header(title=title, subject=subject, paper=paper,
                duration=duration, max_marks=max_marks, date=date),
        _instructions(instructions),
    ]
    num = 0
    total = sum(len(p.questions) for p in parts)
    for part in parts:
        if part.newpage:
            body.append(r"\newpage")
        body.append(_part_head(part))
        if part.lead:
            body.append(r"%s\par\vspace{10pt}" % part.lead)
        for q in part.questions:
            num += 1
            body.append(_question(num, q, figs.get(num, "")))
            if num < total:  # a rule after the last question would strand a page
                body.append(r"\probrule")
    body.append(r"\end{document}")
    return "\n".join(b for b in body if b) + "\n"
