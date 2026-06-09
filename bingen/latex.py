"""Assemble the binary worksheet + answer key (two separate documents)."""

from __future__ import annotations

import wsbase

from boolgen import latex as _bool_latex
from boolgen.problem import Problem as _BoolProblem
from flowgen import latex as _flow_latex
from flowgen.problem import Problem as _FlowProblem

from . import pixel
from .binary import ascii_label, encode, expansion, from_binary, to_binary
from .convert import BASE_NAME, format_value, parse_value, tex_value, working
from .problem import Problem

_BITMAP_INTRO = (
    r"A black-and-white picture is a grid of \emph{pixels}: each pixel is one "
    r"bit --- $1$ means a filled (black) square, $0$ means blank. Each row of 8 "
    r"pixels is one byte, given below in hexadecimal. Convert each byte to 8-bit "
    r"binary, then shade a square wherever there is a $1$.")

# a square pixel cell: 0.5cm wide x 0.5cm tall (sized by invisible rules)
_CELL = r"\rule{0.5cm}{0pt}\rule[-3pt]{0pt}{0.5cm}"

# Worksheet 3 is binary-focused but sprinkles in a couple of Boolean-algebra
# questions and a flowchart trace for revision. Rather than a generic multi-topic
# engine, we just reuse the existing boolgen/flowgen block renderers for those
# few embedded problems (see _dispatch_block). The preamble therefore unions the
# packages all three generators need (listings is flowgen's; amsmath/enumitem are
# boolgen's; needspace/array/\blank are ours).
_PREAMBLE = wsbase.preamble(r"""\usepackage{amsmath}
\usepackage{enumitem}
\usepackage{listings}
\usepackage{needspace}
\usepackage{array}
\lstset{basicstyle=\ttfamily\small, frame=single, framesep=4pt, xleftmargin=4pt,
        columns=fullflexible, keepspaces=true, aboveskip=2pt, belowskip=2pt}
\newcommand{\blank}[1][2.4cm]{\rule[-2pt]{#1}{0.4pt}}
""")


def _esc(v) -> str:
    """Escape a value for LaTeX text (handles every printable ASCII symbol)."""
    s = str(v)
    out = []
    for ch in s:
        out.append({
            "\\": r"\textbackslash{}", "^": r"\textasciicircum{}",
            "~": r"\textasciitilde{}",
            "&": r"\&", "%": r"\%", "#": r"\#", "_": r"\_",
            "{": r"\{", "}": r"\}", "$": r"\$",
        }.get(ch, ch))
    return "".join(out)


def _cell(ch: str) -> str:
    """A single decoded character for a table cell — a literal space is shown
    visibly so the student can see the message contains one."""
    return r"\textvisiblespace{}" if ch == " " else _esc(ch)


# ---- ASCII reference table ---------------------------------------------------

def _ascii_table() -> str:
    """The full 0..127 ASCII chart: 8 column-groups of (decimal, label),
    rows 0..15 — the same layout students get on a printed reference card."""
    group = r"r@{\;\;}>{\ttfamily}l"
    spec = ("@{}" + r"@{\hspace{14pt}}".join([group] * 8) + "@{}")
    rows = []
    for r in range(16):
        cells = []
        for g in range(8):
            code = g * 16 + r
            cells.append("%d & %s" % (code, _esc(ascii_label(code))))
        rows.append(" & ".join(cells) + r" \\")
    return "\n".join([
        r"\begin{center}\footnotesize",
        r"\setlength{\tabcolsep}{2pt}",
        r"\begin{tabular}{%s}" % spec,
        r"\toprule",
        *rows,
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{center}",
    ])


def _reference_section() -> list[str]:
    return [
        r"\subsection*{ASCII reference}",
        r"Each character has a number (its \emph{ASCII code}). Use this table "
        r"wherever a question asks you to decode a message.",
        r"\par\vspace{4pt}",
        _ascii_table(),
        r"\probrule",
    ]


# ---- problem renderers -------------------------------------------------------

def _todecimal(problem: Problem, *, answer: bool) -> list[str]:
    parts = [r"Convert each binary number to decimal:", r"\par\vspace{8pt}"]
    for bits in problem.binaries:
        line = r"\texttt{%s}$_2$ \;=\; " % bits
        if answer:
            contribs, total = expansion(bits)
            working = " + ".join(str(v) for v in contribs) if contribs else "0"
            line += "$%s = \\mathbf{%d}$" % (working, total)
        else:
            line += r"\blank"
        parts.append(line + r"\par\vspace{12pt}")
    return parts


def _tobinary(problem: Problem, *, answer: bool) -> list[str]:
    parts = [r"Convert each decimal number to binary:", r"\par\vspace{8pt}"]
    for n in problem.decimals:
        bits = to_binary(n, problem.width) if problem.width else format(n, "b")
        line = r"$%d$ \;=\; " % n
        if answer:
            contribs, _ = expansion(bits)
            working = " + ".join(str(v) for v in contribs) if contribs else "0"
            line += r"$%s$ \;=\; \texttt{%s}$_2$" % (working, bits)
        else:
            line += r"\blank"
        parts.append(line + r"\par\vspace{12pt}")
    return parts


def _convert(problem: Problem, *, answer: bool) -> list[str]:
    frm, to = problem.frm, problem.to
    parts = [r"Convert each %s number to %s:" % (BASE_NAME[frm], BASE_NAME[to]),
             r"\par\vspace{8pt}"]
    for v in problem.values:
        n = parse_value(v, frm)
        line = r"%s \;=\; " % tex_value(format_value(n, frm), frm)
        if answer:
            mid = working(v, frm, to)
            line += (mid + r" \;=\; " if mid else "") + tex_value(format_value(n, to), to)
        else:
            line += r"\blank"
        parts.append(line + r"\par\vspace{12pt}")
    return parts


def _bitmap(problem: Problem, *, answer: bool) -> list[str]:
    grid = [pixel.to_bits(r) for r in problem.rows]
    w = len(grid[0])
    last_col = 3 + w  # cols: hex | = | binary | <w pixel cells>
    parts = [problem.description or _BITMAP_INTRO, r"\par\vspace{12pt}",
             r"\begin{center}\setlength{\tabcolsep}{0pt}"]
    colspec = r"r@{\hspace{3pt}}c@{\hspace{3pt}}l@{\hspace{14pt}}|" + "c|" * w
    parts += [r"\begin{tabular}{%s}" % colspec, r"\cline{4-%d}" % last_col]
    for bits in grid:
        binary = (r"\texttt{%s}" % pixel.row_bin(bits)) if answer else r"\blank[2.7cm]"
        cells = [(r"\cellcolor{black}" + _CELL) if (answer and b) else _CELL
                 for b in bits]
        parts.append(r"\texttt{%s}$_{16}$ & {=} & %s & %s \\ \cline{4-%d}" % (
            pixel.row_hex(bits), binary, " & ".join(cells), last_col))
    parts += [r"\end{tabular}\end{center}"]
    if problem.reflect:
        parts.append(r"\par\vspace{4pt}\textit{%s}" % _esc(problem.reflect))
    if answer and problem.name:
        parts.append(r"\par\vspace{6pt}\textbf{The picture:}\quad %s" % _esc(problem.name))
    return parts


_IPV4_INTRO = (
    r"Every device on a network has an \emph{IP address}: four numbers separated "
    r"by dots, each stored in one byte (so $0$ to $255$). Convert each part of "
    r"these addresses to 8-bit binary.")


def _bad_ip(addr: str) -> str:
    """Why `addr` is not a valid IPv4 address, or '' if it is fine."""
    octs = addr.split(".")
    if len(octs) != 4:
        return "an address needs four parts"
    for o in octs:
        if not o.isdigit() or int(o) > 255:
            return "%s is more than 255 — too big for one byte" % o
    return ""


def _ipv4(problem: Problem, *, answer: bool) -> list[str]:
    parts = [problem.description or _IPV4_INTRO, r"\par\vspace{10pt}"]
    for addr in problem.values:
        if answer:
            rhs = r"\texttt{%s}" % ".".join(
                format(int(o), "08b") for o in addr.split("."))
        else:
            rhs = r" . ".join([r"\blank[1.9cm]"] * 4)
        parts.append(r"\texttt{%s} \;=\; %s\par\vspace{12pt}" % (addr, rhs))
    if problem.spot:
        parts.append(r"\par\vspace{2pt}Which one of these could \emph{not} be a "
                     r"real IP address, and why?\par\vspace{5pt}")
        parts.append(r"\quad " + r"\qquad ".join(
            r"\texttt{%s}" % s for s in problem.spot))
        if answer:
            why = "; ".join("%s (%s)" % (s, _bad_ip(s))
                            for s in problem.spot if _bad_ip(s))
            parts.append(r"\par\vspace{5pt}\textbf{Answer:}\quad %s" % _esc(why))
        else:
            parts.append(r"\par\vspace{36pt}")
    if problem.reflect:
        parts.append(r"\par\vspace{2pt}\textit{%s}" % _esc(problem.reflect))
    return parts


def _decode(problem: Problem, *, answer: bool) -> list[str]:
    rows = encode(problem.message, problem.width)
    n = len(rows)
    spec = "l|" + "c" * n
    head = r"\begin{center}\ttfamily\small\begin{tabular}{%s}\toprule" % spec

    binary_row = r"\textrm{binary} & " + " & ".join(b for b, _, _ in rows) + r" \\"
    if answer:
        dec_cells = " & ".join(str(d) for _, d, _ in rows)
        let_cells = " & ".join(_cell(c) for _, _, c in rows)
    else:
        blank = " & ".join([r"\rule{0pt}{2.8ex}"] * n)
        dec_cells = let_cells = blank
    dec_row = r"\textrm{decimal} & " + dec_cells + r" \\"
    let_row = r"\textrm{letter} & " + let_cells + r" \\"

    parts = [
        r"Each character of a secret message has been written as its ASCII code "
        r"in %d-bit binary. Convert each code to decimal, then use the ASCII "
        r"table on the first page to decode the message." % problem.width,
        r"\par\vspace{8pt}",
        head, binary_row, r"\midrule", dec_row, let_row,
        r"\bottomrule\end{tabular}\end{center}",
    ]
    if answer:
        parts.append(r"\textbf{Message:}\quad \texttt{%s}" % _esc(problem.message))
    else:
        parts.append(r"\vspace{6pt}\par\textbf{Message:}\quad \blank[7cm]")
    return parts


def _problem_block(idx: int, problem: Problem, *, answer: bool) -> str:
    # the bitmap (intro + 8-row pixel grid) must not split across a page, but
    # reserve only what it needs (~0.4) so it can pack into leftover space
    reserve = "0.4" if problem.kind == "bitmap" else "0.18"
    parts = [r"\Needspace*{%s\textheight}" % reserve, r"\subsection*{Problem %d.}" % idx]
    if problem.description and problem.kind != "bitmap":  # bitmap uses it as its intro
        parts.append(r"\begin{quote}\itshape %s\end{quote}" % _esc(problem.description))
    if problem.kind == "todecimal":
        parts += _todecimal(problem, answer=answer)
    elif problem.kind == "tobinary":
        parts += _tobinary(problem, answer=answer)
    elif problem.kind == "convert":
        parts += _convert(problem, answer=answer)
    elif problem.kind == "bitmap":
        parts += _bitmap(problem, answer=answer)
    elif problem.kind == "ipv4":
        parts += _ipv4(problem, answer=answer)
    elif problem.kind == "decode":
        parts += _decode(problem, answer=answer)
    if problem.note:
        parts.append(r"\par\vspace{2pt}\textit{%s}" % _esc(problem.note))
    return "\n".join(parts)


# ---- document ----------------------------------------------------------------

def _dispatch_block(idx: int, problem, fig_stem, *, answer: bool) -> str:
    """Render one problem, delegating Boolean/flowchart revision questions to
    their own generator's block renderer (reuse, not reimplementation)."""
    fig = (fig_stem + ".pdf") if fig_stem else ""
    if isinstance(problem, Problem):                 # bingen: binary / decode
        return _problem_block(idx, problem, answer=answer)
    if isinstance(problem, _BoolProblem):            # boolgen: gate / truth table
        return _bool_latex._problem_block(idx, problem, fig, answer=answer)
    if isinstance(problem, _FlowProblem):            # flowgen: flowchart trace
        return _flow_latex._problem_block(idx, problem, fig, answer=answer)
    raise TypeError(f"unknown problem type: {type(problem)!r}")


def build_document(rendered, *, title: str, answer_key: bool) -> str:
    """rendered: list of (problem, fig_stem | None). Returns full .tex source."""
    body = [_PREAMBLE, r"\begin{document}", r"\wstitle{%s}" % title]
    if answer_key:
        body.append(r"\textit{Answer key}\par\vspace{8pt}")
    if any(isinstance(p, Problem) and p.kind == "decode" for p, _ in rendered):
        body += _reference_section()
    for i, (problem, fig_stem) in enumerate(rendered, 1):
        body.append(_dispatch_block(i, problem, fig_stem, answer=answer_key))
        body.append(r"\probrule")
    body.append(r"\end{document}")
    return "\n".join(body)
