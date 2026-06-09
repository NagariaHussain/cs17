"""Emit engineering-notation LaTeX for expressions, and assemble worksheets.

Engineering / textbook Boolean notation (what CS students see on a logic-gate
sheet), NOT the math ∧∨¬ notation:

    AND   -> juxtaposition / \\cdot       (A B)
    OR    -> +                            (A + B)
    NOT   -> overbar                      (\\overline{A})
    XOR   -> \\oplus                       (A \\oplus B)
    NAND  -> \\overline{A B}
    NOR   -> \\overline{A + B}
    XNOR  -> \\overline{A \\oplus B}
"""

from __future__ import annotations

from .. import wsbase

from .expr import Expr, Gate, Var, truth_table
from .simplify import simplify

# precedence for deciding when to parenthesise a child
_PREC = {"OR": 1, "NOR": 1, "XOR": 2, "XNOR": 2, "AND": 3, "NAND": 3, "NOT": 4, "VAR": 5}


def _prec(e: Expr) -> int:
    return _PREC["VAR"] if isinstance(e, Var) else _PREC[e.op]


def expr_latex(e: Expr) -> str:
    """Render an Expr as engineering-notation LaTeX (no surrounding $)."""
    if isinstance(e, Var):
        return e.name.upper()

    def wrap(child: Expr, parent_prec: int) -> str:
        s = expr_latex(child)
        return f"({s})" if _prec(child) < parent_prec else s

    op = e.op
    if op == "NOT":
        return r"\overline{%s}" % expr_latex(e.args[0])
    if op in ("AND", "OR", "XOR"):
        sep = {"AND": r" \cdot ", "OR": " + ", "XOR": r" \oplus "}[op]
        return sep.join(wrap(a, _PREC[op]) for a in e.args)
    if op in ("NAND", "NOR", "XNOR"):
        inner_op = {"NAND": "AND", "NOR": "OR", "XNOR": "XOR"}[op]
        sep = {"AND": r" \cdot ", "OR": " + ", "XOR": r" \oplus "}[inner_op]
        body = sep.join(wrap(a, _PREC[inner_op]) for a in e.args)
        return r"\overline{%s}" % body
    raise AssertionError(op)


def truth_table_latex(e: Expr, *, fill: bool, out: str = "Y") -> str:
    """A booktabs truth table. If fill=False, the output column is left blank."""
    vars_, rows = truth_table(e)
    ncol = len(vars_) + 1
    head = " & ".join([v.upper() for v in vars_] + [out])
    spec = "c" * len(vars_) + "|c"
    lines = [r"\begin{tabular}{%s}" % spec, r"\toprule", head + r" \\", r"\midrule"]
    for bits, o in rows:
        cells = [str(b) for b in bits] + [str(o) if fill else r"\rule{0pt}{2.4ex}"]
        lines.append(" & ".join(cells) + r" \\")
    lines += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(lines)


_PREAMBLE = wsbase.preamble(r"""\usepackage{amsmath}
\usepackage{enumitem}
""")


def _fig(path):
    return r"\begin{center}\includegraphics[max width=0.75\linewidth]{%s}\end{center}" % path


def _answer_expr_and_tt(e):
    out = [r"\textbf{Expression:}\quad $%s$" % expr_latex(e)]
    simp = simplify(e)
    if expr_latex(simp) != expr_latex(e):
        out.append(r"\par\textbf{Simplifies to:}\quad $%s$" % expr_latex(simp))
    out.append(r"\vspace{6pt}\par\textbf{Truth table:}\par\nopagebreak\vspace{4pt}")
    out.append(r"\begin{center}" + truth_table_latex(e, fill=True) + r"\end{center}")
    return out


def _problem_block(idx, problem, fig_path, *, answer: bool) -> str:
    head = (" " + problem.title) if problem.title else ""
    parts = [r"\subsection*{Problem %d.%s}" % (idx, head)]
    e, kind = problem.expr, problem.kind

    if kind == "diagram":
        parts.append(_fig(fig_path))
        if answer:
            parts += _answer_expr_and_tt(e)
        else:
            parts.append(r"Write the Boolean expression for output $Y$, then draw its truth table.")

    elif kind == "circuit":
        parts.append(r"Draw the logic-gate circuit for:")
        parts.append(r"\[ Y = %s \]" % expr_latex(e))
        if answer:
            parts.append(_fig(fig_path))
        else:
            parts.append(r"\vspace{90pt}\par")

    elif kind == "truthtable":
        parts.append(r"Draw the truth table for:")
        parts.append(r"\[ Y = %s \]" % expr_latex(e))
        if answer:
            parts.append(r"\begin{center}" + truth_table_latex(e, fill=True) + r"\end{center}")
        else:
            parts.append(r"\vspace{6pt}\par")

    return "\n".join(parts)


def _section(rendered, *, title, answer_key):
    """rendered: list of (Problem, fig_path | None)."""
    out = [r"\wstitle{%s}" % title]
    if answer_key:
        out.append(r"\textit{Answer key}\par\vspace{8pt}")
    else:
        # quick reminder of the XOR identity for revision
        out.append(r"\fbox{Reminder:\quad $A \oplus B = \overline{A}\,B + A\,\overline{B}$ \quad(XOR)}"
                   r"\par\vspace{10pt}")
    for i, (problem, fig) in enumerate(rendered, 1):
        fig_path = (fig + ".pdf") if fig else ""
        out.append(_problem_block(i, problem, fig_path, answer=answer_key))
        out.append(r"\probrule")
    return out


def build_document(rendered, *, title: str, answer_key: bool) -> str:
    """One document — the worksheet, or (separately) the answer key.

    rendered: list of (Problem, fig_path_stem | None). Returns full .tex source.
    """
    body = [_PREAMBLE, r"\begin{document}"]
    body += _section(rendered, title=title, answer_key=answer_key)
    body.append(r"\end{document}")
    return "\n".join(body)
