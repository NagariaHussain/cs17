"""Assemble the flowchart worksheet + answer key (two separate documents)."""

from __future__ import annotations

from .. import wsbase

from .algo import Algorithm, pseudocode_lines, pseudocode_text, run
from .bug import outcome
from .scratch import scratch_blocks

_PREAMBLE = wsbase.preamble(r"""\usepackage{listings}
\usepackage{needspace}
\usepackage{scratch3}
\setdefaultscratch{else word=else}
% repeat-until as a clean C-block with no loop arrow (Scratch's repeat-until has
% none): the package's internal loop macro, args {text}{body}{else}{infinite}{arrow}.
\newcommand\blockrepeatuntil[2]{\csname scr_blockloop\endcsname{#1}{#2}{}00}
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


def _draw_space(algo: Algorithm) -> str:
    """A framed, blank box for the student to draw the flowchart in (the sheets
    are submitted, so they draw on the sheet itself). Its height scales with the
    algorithm's size — a straight-line sequence gets less room, a loop with a
    decision inside gets more — clamped so one problem never overruns a page."""
    n = len(pseudocode_lines(algo))
    height = min(500, max(300, 55 * n + 130))
    return (r"\par\vspace{6pt}\begin{center}\fbox{"
            + (r"\begin{minipage}[t][%dpt][t]{0.92\linewidth}" % height)
            + r"\textcolor{gray!70}{\footnotesize\itshape Draw your flowchart in "
              r"this box (rough work in your notebook first).}"
            + r"\end{minipage}}\end{center}")


def _trace_table(cols, rows, *, fill: bool, row_height: str = "3.4ex",
                 n_rows: int | None = None) -> str:
    """`row_height` / `n_rows` tune the blank version — an exam page is tighter
    than a worksheet's, so examgen asks for shorter rows and exactly as many as
    the trace needs (see gens/examgen/latex.py)."""
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
        blank_row = " & ".join([r"\rule{0pt}{%s}" % row_height] * (len(cols) + 1)) + r" \\"
        n_rows = n_rows or max(6, len(rows) + 2)
        out += [blank_row + (r" \hline" if i < n_rows - 1 else "")
                for i in range(n_rows)]
        out += [r"\arrayrulecolor{black}", r"\bottomrule", r"\end{tabular}"]
    return "\n".join(out)


def _trace_instruction(inputs: dict, noun: str = "algorithm",
                       closing: str = "and complete the trace table") -> str:
    """E.g. 'Trace this algorithm for $n = 3$, where the values of $marks$
    entered are 55, 82, 40 (in that order), and complete the trace table.'

    `closing` is the last clause: a worksheet prints a blank table to complete,
    an exam paper (examgen) prints none, so the student draws it."""
    scalars = {k: v for k, v in inputs.items() if not isinstance(v, (list, tuple))}
    arrays = {k: v for k, v in inputs.items() if isinstance(v, tuple)}
    queues = {k: v for k, v in inputs.items() if isinstance(v, list)}
    text = r"Trace this %s" % noun
    if scalars:
        text += r" for $%s$" % _esc(", ".join(f"{k} = {v}" for k, v in scalars.items()))
    for k, vals in arrays.items():  # a given array (constant, indexed by the algorithm)
        listed = "[" + ", ".join(str(v) for v in vals) + "]"
        text += r", taking the list $%s$ to be %s" % (_esc(k), _esc(listed))
    for k, vals in queues.items():
        text += r", where the values of $%s$ entered are %s (in that order)" % (
            _esc(k), _esc(", ".join(str(v) for v in vals)))
    return f"{text}, {closing}."


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


def _scratch_beside_trace(algo, cols, rows, *, fill: bool) -> list:
    """Scratch script and trace table side by side — the Scratch counterpart of
    _fig_beside_trace, used when a problem presents the program as blocks."""
    return [
        r"\par\vspace{8pt}",
        r"\begin{minipage}[c]{0.46\linewidth}\centering",
        scratch_blocks(algo, scale=0.7),
        r"\end{minipage}\hfill",
        r"\begin{minipage}[c]{0.5\linewidth}\centering",
        _trace_table(cols, rows, fill=fill),
        r"\end{minipage}",
    ]


def _scratch_centered(algo) -> str:
    return r"\begin{center}" + scratch_blocks(algo, scale=0.82) + r"\end{center}"


def _fixed_path(fig_path: str) -> str:
    """The answer key's corrected flowchart sits beside the buggy one."""
    return fig_path.replace(".pdf", "-fixed.pdf")


def _case_text(case: dict) -> str:
    """One input case as text: 'n = 3, x = 10, 20, 30'."""
    bits = []
    for k, v in case.items():
        listed = ", ".join(str(x) for x in v) if isinstance(v, (list, tuple)) else str(v)
        bits.append(f"{k} = {listed}")
    return ", ".join(bits)


def _outputs_text(outputs, never_stops: bool) -> str:
    """Printed values as the sheet shows them — a runaway loop is cut short and
    labelled, since 'prints 1 for ever' IS the symptom."""
    shown = outputs[:5] if never_stops else outputs
    text = ", ".join(_esc(o) for o in shown)
    if never_stops:
        return (text + r", \dots{} \textit{(never stops)}" if text
                else r"\textit{nothing --- it never stops}")
    return text or r"\textit{nothing}"


def _symptom_table(problem) -> str:
    """What the program should print vs what it actually prints, for each input:
    both sides are run, so the symptom can never disagree with the flowchart."""
    col = lambda w: r">{\raggedright\arraybackslash}p{%s}" % w
    out = [r"\begin{tabular}{%s|%s|%s}" % (col("3.4cm"), col("4.2cm"), col("4.2cm")),
           r"\toprule",
           r"input & should print & actually prints \\", r"\midrule"]
    for case in problem.cases:
        should, _ = outcome(problem.algo, case)
        actual, never_stops = outcome(problem.broken, case)
        out.append(" & ".join([_esc(_case_text(case)), _outputs_text(should, False),
                               _outputs_text(actual, never_stops)]) + r" \\")
    out += [r"\bottomrule", r"\end{tabular}"]
    return "\n".join(out)


def _fix_text(problem) -> str:
    """The answer: which box is wrong and what it should say. The mutator that
    planted the bug reports it (see bug.FIXES), so this only phrases it."""
    kind, *rest = problem.fix
    box = lambda s: r"\texttt{%s}" % _esc(s)
    if kind == "replace":
        wrong, right = rest
        return "the box %s should be %s" % (box(wrong), box(right))
    if kind == "missing":
        missing_box, where = rest
        return "the box %s is missing%s" % (box(missing_box),
                                            (" " + where) if where else "")
    if kind == "moved":
        moved_box, belongs = rest
        return ("the box %s has been drawn inside the loop --- it belongs %s"
                % (box(moved_box), belongs))
    if kind == "swapped":
        cond, yes, no = rest
        return ("the Yes and No arms of the decision %s are the wrong way round: "
                "Yes should lead to %s and No to %s"
                % (box(cond), box(yes), box(no)))
    raise AssertionError(problem.fix)


def _answer_lines(*prompts) -> str:
    """Ruled blanks for the student's answer (the sheets are handed in)."""
    return "\n".join(
        r"\par\vspace{8pt}\textbf{%s}~%s~\rule[-0.35em]{%s}{0.4pt}" % (label, text, width)
        for label, text, width in prompts)


def _debug_block(problem, fig_path, *, answer: bool) -> list:
    parts = [r"\begin{quote}\itshape %s\end{quote}" % _esc(problem.description)]
    if problem.note:
        parts.append(r"\par\vspace{2pt}\textit{%s}" % _esc(problem.note))
    # chart above, symptom table below (not side by side): a chart with a
    # decision inside a loop comes out WIDE, and a narrow column squashes it
    parts += [
        r"\par\vspace{8pt}\begin{center}",
        r"\includegraphics[max width=\linewidth,"
        r"max totalheight=0.4\textheight]{%s}" % (
            _fixed_path(fig_path) if answer else fig_path),
        r"\par\vspace{10pt}",
        _symptom_table(problem),
        r"\end{center}",
    ]
    if answer:
        parts.append(r"\par\vspace{8pt}\textbf{The mistake:}\quad %s."
                     % _fix_text(problem))
        if problem.why:
            parts.append(r"\par\vspace{2pt}\textit{%s}" % _esc(problem.why))
        parts.append(r"\par\vspace{2pt}\textit{(The flowchart above is the "
                     r"corrected one.)}")
    else:
        parts.append(_answer_lines(
            ("(i)", "Which box is wrong? Copy it here:", "6cm"),
            ("(ii)", "What should that box say instead?", "6cm")))
        # the prompt and its two writing lines are one unit: a page break
        # between them would leave a stray rule at the top of the next page
        parts.append(r"\par\vspace{8pt}\begin{minipage}{\linewidth}"
                     r"\textbf{(iii)}~Why does that mistake produce the wrong "
                     r"output?"
                     r"\par\vspace{14pt}\rule{\linewidth}{0.4pt}"
                     r"\par\vspace{14pt}\rule{\linewidth}{0.4pt}"
                     r"\end{minipage}")
    return parts


def _problem_block(idx, problem, fig_path, *, answer: bool) -> str:
    parts = []
    if problem.kind == "trace" or (problem.kind == "outputs" and problem.inputs):
        # heading + flowchart/table block must stay together
        parts.append(r"\Needspace*{0.78\textheight}")
    elif problem.kind == "draw" and problem.cases:
        # statement + worked example + predict table should not split
        parts.append(r"\Needspace*{0.5\textheight}")
    elif problem.kind == "debug":
        # statement + chart + symptom table + answer space is a whole page's
        # worth: keep it together rather than letting the ruled lines spill over
        parts.append(r"\Needspace*{0.75\textheight}")
    parts.append(r"\subsection*{Problem %d.}" % idx)
    algo = problem.algo
    noun = "Scratch program" if problem.present == "scratch" else "algorithm"

    if problem.kind == "debug":
        parts += _debug_block(problem, fig_path, answer=answer)

    elif problem.kind == "draw":
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
            parts.append(_draw_space(algo))
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
        parts.append(_trace_instruction(problem.inputs, noun))
        if problem.note:
            parts.append(r"\par\vspace{2pt}\textit{%s}" % _esc(problem.note))
        if problem.present == "scratch":
            parts += _scratch_beside_trace(algo, cols, rows, fill=answer)
        else:
            parts += _fig_beside_trace(fig_path, cols, rows, fill=answer)
        if answer:
            shown = ", ".join(_esc(o) for o in outputs)
            parts.append(r"\textbf{Output:}\quad %s" % (shown or r"\textit{(none)}"))
        if problem.reveal:  # real-world tie-in, shown only after the trace table
            parts.append(r"\par\vspace{6pt}\textit{%s}" % _esc(problem.reveal))

    elif problem.kind == "outputs":
        has_trace = bool(problem.inputs)
        n_parts = 1 + has_trace + bool(problem.followup)
        labels = iter([r"(i)~", r"(ii)~", r"(iii)~"] if n_parts > 1 else ["", "", ""])
        if has_trace:  # warm-up: trace one input, program beside the table
            cols, rows, _ = run(algo, problem.inputs)
            parts.append(next(labels) + _trace_instruction(problem.inputs, noun))
            if problem.note:
                parts.append(r"\par\vspace{2pt}\textit{%s}" % _esc(problem.note))
            if problem.present == "scratch":
                parts += _scratch_beside_trace(algo, cols, rows, fill=answer)
            else:
                parts += _fig_beside_trace(fig_path, cols, rows, fill=answer)
            parts.append(r"\par\vspace{8pt}")
        elif problem.present == "scratch":
            parts.append(_scratch_centered(algo))
        else:
            parts.append(_fig(fig_path))
        follow = "Scratch program" if problem.present == "scratch" else "flowchart"
        parts.append(next(labels)
                     + r"For each input below, follow the %s and write the output." % follow)
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


def _section(rendered, *, title, answer_key, lead=""):
    out = [r"\wstitle{%s}" % title]
    if answer_key:
        out.append(r"\textit{Answer key}\par\vspace{8pt}")
    else:
        out.append(r"\wsnamefield")
    if lead and not answer_key:  # how to attempt the sheet — students only
        out.append(r"%s\par\vspace{10pt}" % lead)
    for i, (problem, fig) in enumerate(rendered, 1):
        out.append(_problem_block(i, problem, (fig + ".pdf") if fig else "", answer=answer_key))
        out.append(r"\probrule")
    return out


def build_document(rendered, *, title: str, answer_key: bool, lead: str = "") -> str:
    """rendered: list of (Problem, fig_path_stem). Returns full .tex source."""
    body = [_PREAMBLE, r"\begin{document}"]
    body += _section(rendered, title=title, answer_key=answer_key, lead=lead)
    body.append(r"\end{document}")
    return "\n".join(body)
