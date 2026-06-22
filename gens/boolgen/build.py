"""CLI: turn a problem-set module into worksheet + answer-key PDFs.

Usage:
    python -m boolgen.build sets/set01.py
    python -m boolgen.build sets/set01.py --out build --no-pdf

A problem-set module defines a module-level list `PROBLEMS` and optional `TITLE`:

    from boolgen import parse
    TITLE = "CS17 - Boolean Algebra - Set 1"
    PROBLEMS = [
        ("Majority", parse("(a & b) | (b & c) | (a & c)")),
        ("Half adder carry", parse("a & b")),
    ]
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from .. import wsbase
from ..flowgen.flowchart import render as _render_flow
from ..flowgen.problem import Problem as _FlowProblem

from . import latex
from .diagram import render
from .expr import variables
from .problem import Problem, DIAGRAM

# Boolean problem kinds that SHOW a circuit and so need a rendered figure: the
# gate diagram (worksheet for `diagram`, answer key for `circuit`/`fromtable`).
_FIG_KINDS = ("diagram", "circuit", "fromtable")


def _normalize(item) -> Problem:
    """Accept a Problem, a bare expression (-> DIAGRAM), or (title, expr).

    Flowchart-tracing problems (a flowgen Problem) are a boolgen-hosted sheet's
    revision questions; they pass straight through, handled by their own renderer.
    """
    if isinstance(item, (Problem, _FlowProblem)):
        return item
    if isinstance(item, tuple):
        title, expr = item
        return DIAGRAM(expr, title)
    return DIAGRAM(item)


def _load_set(path: Path):
    spec = importlib.util.spec_from_file_location("_probset", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    title = getattr(mod, "TITLE", path.stem)
    problems = getattr(mod, "PROBLEMS")
    # opt-in per worksheet: show the XOR identity reminder box (Worksheet 1 uses
    # it; sheets where students should derive XOR themselves leave it off)
    xor_reminder = getattr(mod, "XOR_REMINDER", False)
    return title, problems, xor_reminder


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate Boolean-algebra practice PDFs")
    ap.add_argument("set", type=Path, help="path to a problem-set .py module")
    ap.add_argument("--out", type=Path, default=Path("build"), help="output dir")
    ap.add_argument("--no-pdf", action="store_true", help="emit .tex + figures but skip Tectonic")
    args = ap.parse_args(argv)

    title, problems, xor_reminder = _load_set(args.set)
    name = args.set.stem
    figs = args.out / name / "figs"
    figs.mkdir(parents=True, exist_ok=True)
    for stale in figs.glob("p*.*"):  # drop figures from removed problems
        stale.unlink()

    rendered = []  # (Problem, fig_stem | None)
    nfigs = 0
    for i, item in enumerate(problems, 1):
        p = _normalize(item)
        if isinstance(p, _FlowProblem):  # flowchart revision question
            _render_flow(p.algo, str(figs / f"p{i:02d}"))
            rendered.append((p, f"figs/p{i:02d}"))
            nfigs += 1
            continue
        # the table the student must read (truthtable/fromtable) is capped so it
        # stays small enough to reason about by hand
        if p.kind in ("truthtable", "fromtable") and len(variables(p.expr)) > 3:
            raise ValueError(f"problem {i}: truth-table problems are capped at 3 variables")
        fig = None
        if p.kind in _FIG_KINDS:
            render(p.expr, str(figs / f"p{i:02d}"))  # writes pdf + png + svg
            fig = f"figs/p{i:02d}"
            nfigs += 1
        rendered.append((p, fig))
    print(f"rendered {nfigs} diagrams -> {figs}")

    # two separate PDFs: the worksheet, and the answer key
    for suffix, key in (("", False), ("-answers", True)):
        tex = latex.build_document(rendered, title=title, answer_key=key,
                                   xor_reminder=xor_reminder)
        tex_path = args.out / name / f"{name}{suffix}.tex"
        tex_path.write_text(tex)
        print(f"wrote {tex_path}")
        if not args.no_pdf:
            wsbase.compile_tex(tex_path)
            print(f"compiled {tex_path.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
