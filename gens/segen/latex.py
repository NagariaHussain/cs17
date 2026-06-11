"""Assemble the seven-segment worksheet + answer key (two separate documents).

Everything is drawn inline with TikZ from the single source of truth in
`display`, so there are no external figures to render — `build.py` just emits and
compiles the .tex.
"""

from __future__ import annotations

from .. import wsbase

from . import display
from .problem import Problem

_PREAMBLE = wsbase.preamble(r"""\usepackage{tikz}
\usepackage{array}
\newcommand{\bit}[1]{\texttt{#1}}
\newcommand{\blank}[1][2.4cm]{\rule[-2pt]{#1}{0.4pt}}
""")

_INTRO = (
    r"A \emph{seven-segment display} shows a digit by lighting up to seven little "
    r"bars, labelled \texttt{a} to \texttt{g}. To draw a digit you switch some "
    r"bars on and leave the rest off --- so the whole display is really just "
    r"\textbf{7 bits}: one bit per bar, where \bit{1} means \emph{on} and "
    r"\bit{0} means \emph{off}. The seven bits for a digit are its row of the "
    r"display's \emph{truth table}.")


def _worked_example(d: int) -> list[str]:
    """One digit shown fully worked — the method, at its simplest."""
    letters = display.lit_letters(d)
    names = ", ".join(r"\texttt{%s}" % s for s in letters[:-1])
    names = "%s and \\texttt{%s}" % (names, letters[-1]) if len(letters) > 1 \
        else r"\texttt{%s}" % letters[0]
    row = " ".join(r"\bit{%d}" % b for b in display.bits(d))
    return [
        r"\textbf{Worked example --- the digit %d.}\quad" % d,
        r"To make a \textbf{%d} you light segments %s; every other bar stays off." % (d, names),
        r"\par\vspace{6pt}",
        r"\begin{center}",
        r"\renewcommand{\arraystretch}{1.3}",
        r"\begin{tabular}{c@{\hspace{20pt}}c}",
        display.glyph(display.LIT[d], scale=0.5) + r" & ",
        r"$\bit{a}\,\bit{b}\,\bit{c}\,\bit{d}\,\bit{e}\,\bit{f}\,\bit{g}"
        r" \;=\; %s$ \\[4pt]" % row,
        r"\end{tabular}",
        r"\end{center}",
        r"Read the bars in order \texttt{a}, \texttt{b}, \dots, \texttt{g} to get "
        r"the seven output bits.",
    ]


def _truth_table(digits, *, answer: bool) -> list[str]:
    head = (r"digit & display & \bit{a} & \bit{b} & \bit{c} & \bit{d} & "
            r"\bit{e} & \bit{f} & \bit{g} \\")
    rows = []
    for d in digits:
        if answer:
            disp = display.glyph(display.LIT[d], scale=0.26)
            cells = " & ".join(
                (r"\cellcolor{black!12}\bit{1}" if b else r"\bit{0}")
                for b in display.bits(d))
        else:
            disp = display.glyph([], scale=0.26)  # faint empty display to shade
            cells = " & ".join([""] * 7)
        rows.append(r"%d & %s & %s \\" % (d, disp, cells))
    stretch = "1.4" if answer else "2.6"
    return [
        r"\begin{center}",
        r"\renewcommand{\arraystretch}{%s}" % stretch,
        r"\setlength{\tabcolsep}{8pt}",
        r"\begin{tabular}{c|c|ccccccc}",
        r"\toprule", head, r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{center}",
    ]


def _sevenseg(problem: Problem, *, answer: bool) -> list[str]:
    parts = [problem.description or _INTRO, r"\par\vspace{12pt}"]
    parts += [r"\begin{center}", display.reference(scale=1.0), r"\end{center}"]
    parts += [r"\par\vspace{6pt}"]
    parts += _worked_example(problem.example)
    parts += [r"\par\vspace{10pt}",
              r"\textbf{Your turn.}\quad For each digit below, shade the bars "
              r"that light up, then write its seven output bits "
              r"(\bit{1} = lit, \bit{0} = off).",
              r"\par\vspace{6pt}"]
    parts += _truth_table(problem.digits, answer=answer)
    if problem.note:
        parts.append(r"\par\vspace{2pt}\textit{%s}" % problem.note)
    return parts


_DECODER_INTRO = (
    r"A display chip can't read the shape ``7'' --- it is handed the digit as a "
    r"\emph{binary number} and must switch on the right bars. (This is how a "
    r"digital clock or a scoreboard lights up its digits.) Each digit arrives as "
    r"binary on the \emph{input}, and the seven segment bits come out as the "
    r"\emph{output}. So this time \textbf{both the input and the output are "
    r"binary numbers.}")


def _decoder(problem: Problem, *, answer: bool) -> list[str]:
    digits = problem.digits
    w = max(max(digits).bit_length(), 1)  # bits needed to count 0..max digit

    parts = [problem.description or _DECODER_INTRO, r"\par\vspace{10pt}"]

    # (a) how many input bits?
    parts.append(r"\textbf{(a)} Every digit must reach the display as a binary "
                 r"number. How many bits do you need to represent every digit "
                 r"from 0 to 9?\quad ")
    if answer:
        parts.append(r"\textbf{%d bits} --- the largest digit is "
                     r"$9 = \bit{1001}$, which already needs 4 bits "
                     r"(3 bits only count up to 7).\par\vspace{10pt}" % w)
    else:
        parts.append(r"\blank[2.2cm]\par\vspace{12pt}")

    # (b) the table
    parts.append(r"\textbf{(b)} Complete the truth table: write each digit as a "
                 r"%d-bit binary \emph{input}, then the seven segment bits "
                 r"(\bit{a}--\bit{g}) it switches on as the \emph{output}." % w)
    parts.append(r"\par\vspace{8pt}")

    place = " & ".join(r"\bit{%d}" % (1 << i) for i in range(w - 1, -1, -1))
    seg_hdr = " & ".join(r"\bit{%s}" % s for s in display.SEGMENTS)
    colspec = "c|" + "c" * w + "|" + "c" * 7
    head1 = (r"\multicolumn{1}{c|}{} & \multicolumn{%d}{c|}{input (binary)} & "
             r"\multicolumn{7}{c}{output (segments)} \\" % w)
    head2 = r"decimal & %s & %s \\" % (place, seg_hdr)

    rows = []
    for d in digits:
        if answer:
            in_cells = " & ".join(r"\bit{%s}" % b for b in format(d, "0%db" % w))
            out_cells = " & ".join(
                (r"\cellcolor{black!12}\bit{1}" if b else r"\bit{0}")
                for b in display.bits(d))
        else:
            in_cells = " & ".join([""] * w)
            out_cells = " & ".join([""] * 7)
        rows.append(r"%d & %s & %s \\" % (d, in_cells, out_cells))

    stretch = "1.5" if answer else "2.3"
    parts += [
        r"\begin{center}",
        r"\renewcommand{\arraystretch}{%s}" % stretch,
        r"\setlength{\tabcolsep}{6pt}",
        r"\begin{tabular}{%s}" % colspec,
        r"\toprule", head1, head2, r"\midrule",
        *rows,
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{center}",
    ]
    if answer:
        parts.append(r"\par\vspace{2pt}\textit{The seven output columns are "
                     r"exactly the rows you found in Problem 1 --- same display, "
                     r"now driven by a binary input.}")
    if problem.note:
        parts.append(r"\par\vspace{2pt}\textit{%s}" % problem.note)
    return parts


def _badge(text: str) -> str:
    """A small difficulty tag shown to the right of a problem heading."""
    return (r"\hfill{\normalfont\footnotesize\sffamily"
            r"\colorbox{black!10}{\,%s\,}}" % text)


def _problem_block(idx: int, problem: Problem, *, answer: bool) -> str:
    tag = _badge(problem.tag) if problem.tag else ""
    parts = [r"\subsection*{Problem %d.%s}" % (idx, tag)]
    if problem.kind == "decoder":
        parts += _decoder(problem, answer=answer)
    else:
        parts += _sevenseg(problem, answer=answer)
    return "\n".join(parts)


def build_document(problems, *, title: str, answer_key: bool) -> str:
    body = [_PREAMBLE, r"\begin{document}", r"\wstitle{%s}" % title]
    if answer_key:
        body.append(r"\textit{Answer key}\par\vspace{8pt}")
    for i, problem in enumerate(problems, 1):
        body.append(_problem_block(i, problem, answer=answer_key))
        body.append(r"\probrule")
    body.append(r"\end{document}")
    return "\n".join(body)
