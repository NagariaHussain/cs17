"""Assemble the flowchart worksheet + answer key (two separate documents)."""

from __future__ import annotations

from .. import wsbase

from .algo import Algorithm, pseudocode_text, run

_PREAMBLE = wsbase.preamble(r"""\usepackage{listings}
\usepackage{needspace}
\lstset{basicstyle=\ttfamily\small, frame=single, framesep=4pt, xleftmargin=4pt,
        columns=fullflexible, keepspaces=true, aboveskip=2pt, belowskip=2pt}
""")


def _esc(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        v = int(v)  # show 7500, not 7500.0 (a whole-rupee result of *0.05 etc.)
    s = str(v)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}")]:
        s = s.replace(a, b)
    return s


def _fig(path, max_height=r"0.72\textheight"):
    return (r"\begin{center}\includegraphics[max width=0.55\linewidth,"
            r"max totalheight=%s]{%s}\end{center}" % (max_height, path))


def _pseudocode(algo: Algorithm) -> str:
    return "\\begin{lstlisting}\n" + pseudocode_text(algo) + "\n\\end{lstlisting}"


def _trace_table(cols, rows, *, fill: bool) -> str:
    header = " & ".join(_esc(c) for c in cols) + r" & output"
    if fill:
        spec = "c" * len(cols) + "|c"
        out = [r"\begin{tabular}{%s}" % spec, r"\toprule", header + r" \\", r"\midrule"]
        for env, o in rows:
            cells = [_esc(env.get(c)) for c in cols] + [_esc(o)]
            out.append(" & ".join(cells) + r" \\")
        out += [r"\bottomrule", r"\end{tabular}"]
    else:
        # blank version: fixed-width columns + light ruled rows to write in
        col = r">{\centering\arraybackslash}p{1.4cm}"
        spec = col * len(cols) + "|" + col
        out = [r"\begin{tabular}{%s}" % spec, r"\toprule", header + r" \\", r"\midrule",
               r"\arrayrulecolor{gray!50}"]
        blank_row = " & ".join([r"\rule{0pt}{3.4ex}"] * (len(cols) + 1)) + r" \\"
        n_rows = max(6, len(rows) + 2)
        out += [blank_row + (r" \hline" if i < n_rows - 1 else "")
                for i in range(n_rows)]
        out += [r"\arrayrulecolor{black}", r"\bottomrule", r"\end{tabular}"]
    return "\n".join(out)


def _trace_instruction(inputs: dict) -> str:
    """E.g. 'Trace this algorithm for $n = 3$, where the values of $marks$
    entered are 55, 82, 40 (in that order), and complete the trace table.'"""
    scalars = {k: v for k, v in inputs.items() if not isinstance(v, list)}
    queues = {k: v for k, v in inputs.items() if isinstance(v, list)}
    text = r"Trace this algorithm"
    if scalars:
        text += r" for $%s$" % _esc(", ".join(f"{k} = {v}" for k, v in scalars.items()))
    for k, vals in queues.items():
        text += r", where the values of $%s$ entered are %s (in that order)" % (
            _esc(k), _esc(", ".join(str(v) for v in vals)))
    return text + ", and complete the trace table."


def _outputs_table(algo: Algorithm, cases, *, fill: bool) -> str:
    in_vars = list(cases[0].keys())
    spec = "c" * len(in_vars) + "|c"
    header = " & ".join(rf"input $%s$" % _esc(v) for v in in_vars) + r" & output"
    out = [r"\begin{tabular}{%s}" % spec, r"\toprule", header + r" \\", r"\midrule"]
    for case in cases:
        cells = [_esc(case[v]) for v in in_vars]
        if fill:
            _, _, outputs = run(algo, case)
            cells.append(", ".join(_esc(o) for o in outputs))
        else:
            cells.append(r"\rule{0pt}{2.6ex}")
        out.append(" & ".join(cells) + r" \\")
    out += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(out)


def _fig_beside_trace(fig_path, cols, rows, *, fill: bool) -> list:
    """Flowchart and trace table side by side (both are tall and narrow)."""
    return [
        r"\par\vspace{8pt}",
        r"\begin{minipage}[c]{0.46\linewidth}",
        r"\includegraphics[max width=\linewidth,"
        r"max totalheight=0.7\textheight]{%s}" % fig_path,
        r"\end{minipage}\hfill",
        r"\begin{minipage}[c]{0.5\linewidth}\centering",
        _trace_table(cols, rows, fill=fill),
        r"\end{minipage}",
    ]


def _problem_block(idx, problem, fig_path, *, answer: bool) -> str:
    parts = []
    if problem.kind == "trace" or (problem.kind == "outputs" and problem.inputs):
        # heading + flowchart/table block must stay together
        parts.append(r"\Needspace*{0.78\textheight}")
    elif problem.kind == "draw" and problem.cases:
        # statement + worked example + predict table should not split
        parts.append(r"\Needspace*{0.5\textheight}")
    parts.append(r"\subsection*{Problem %d.}" % idx)
    algo = problem.algo

    if problem.kind == "draw":
        predict = problem.cases  # inputs to predict the output for, before drawing
        if not answer:
            # the statement comes first — it's needed for both parts
            if problem.description:  # plain English instead of pseudocode
                parts.append(r"\begin{quote}\itshape %s\end{quote}" % _esc(problem.description))
            else:
                parts.append(_pseudocode(algo))
            if predict:
                parts.append(
                    r"\textbf{(i)}~Before drawing anything, work out by hand what "
                    r"the program should print for each input below. (Once you "
                    r"have drawn your flowchart, trace it on these same inputs and "
                    r"check that it agrees with your answers here.)")
                if problem.example:
                    parts.append(r"\par\vspace{2pt}\textit{Worked example: %s}"
                                 % _esc(problem.example))
                parts.append(r"\par\vspace{4pt}\begin{center}"
                             + _outputs_table(algo, predict, fill=False) + r"\end{center}")
                parts.append(r"\textbf{(ii)}~Now draw a flowchart for the algorithm.")
            else:
                parts.append(r"Draw a flowchart for this algorithm:")
            parts.append(r"\vspace{120pt}\par")
        else:
            if predict:
                parts.append(r"\textbf{(i)}~Expected output for each input:"
                             r"\par\vspace{4pt}\begin{center}"
                             + _outputs_table(algo, predict, fill=True) + r"\end{center}")
                parts.append(r"\textbf{(ii)}~Flowchart:\par")
            parts.append(_fig(fig_path))

    elif problem.kind == "trace":
        cols, rows, outputs = run(algo, problem.inputs)
        if problem.description:  # written use case before the flowchart
            parts.append(r"\begin{quote}\itshape %s\end{quote}" % _esc(problem.description))
        parts.append(_trace_instruction(problem.inputs))
        if problem.note:
            parts.append(r"\par\vspace{2pt}\textit{%s}" % _esc(problem.note))
        parts += _fig_beside_trace(fig_path, cols, rows, fill=answer)
        if answer:
            shown = ", ".join(_esc(o) for o in outputs)
            parts.append(r"\textbf{Output:}\quad %s" % (shown or r"\textit{(none)}"))

    elif problem.kind == "outputs":
        has_trace = bool(problem.inputs)
        n_parts = 1 + has_trace + bool(problem.followup)
        labels = iter([r"(i)~", r"(ii)~", r"(iii)~"] if n_parts > 1 else ["", "", ""])
        if has_trace:  # warm-up: trace one input, flowchart beside the table
            cols, rows, _ = run(algo, problem.inputs)
            parts.append(next(labels) + _trace_instruction(problem.inputs))
            if problem.note:
                parts.append(r"\par\vspace{2pt}\textit{%s}" % _esc(problem.note))
            parts += _fig_beside_trace(fig_path, cols, rows, fill=answer)
            parts.append(r"\par\vspace{8pt}")
        else:
            parts.append(_fig(fig_path))
        parts.append(next(labels)
                     + r"For each input below, follow the flowchart and write the output.")
        if problem.note and not has_trace:
            parts.append(r"\par\vspace{2pt}\textit{%s}" % _esc(problem.note))
        parts.append(r"\par\vspace{4pt}")
        parts.append(r"\begin{center}" + _outputs_table(algo, problem.cases, fill=answer)
                     + r"\end{center}")
        if problem.followup:
            parts.append(next(labels) + _esc(problem.followup))
            if answer:
                # the algorithm's title is the single-source answer to "what does it do?"
                parts.append(r"\par\vspace{4pt}\textbf{Answer:}\quad %s" % _esc(algo.title))
            else:
                parts.append(r"\par\vspace{50pt}")

    return "\n".join(parts)


def _section(rendered, *, title, answer_key):
    out = [r"\wstitle{%s}" % title]
    if answer_key:
        out.append(r"\textit{Answer key}\par\vspace{8pt}")
    for i, (problem, fig) in enumerate(rendered, 1):
        out.append(_problem_block(i, problem, (fig + ".pdf") if fig else "", answer=answer_key))
        out.append(r"\probrule")
    return out


def build_document(rendered, *, title: str, answer_key: bool) -> str:
    """rendered: list of (Problem, fig_path_stem). Returns full .tex source."""
    body = [_PREAMBLE, r"\begin{document}"]
    body += _section(rendered, title=title, answer_key=answer_key)
    body.append(r"\end{document}")
    return "\n".join(body)
