"""CLI: turn a binary worksheet module into worksheet + answer-key PDFs.

Usage:
    python -m bingen.build binary_worksheet.py
    python -m bingen.build binary_worksheet.py --out build --no-pdf

The module defines TITLE and a list PROBLEMS. Binary problems (TODECIMAL /
DECODE) are typeset directly and carry no figure. The sheet may also include a
few Boolean-algebra and flowchart problems for revision — those reuse boolgen's
and flowgen's renderers, so they DO need a figure (the gate diagram / flowchart),
which is rendered into figs/ here just like in those generators.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import wsbase
from boolgen.diagram import render as _render_circuit
from boolgen.problem import Problem as _BoolProblem
from flowgen.flowchart import render as _render_flow
from flowgen.problem import Problem as _FlowProblem

from . import latex


def _load(path: Path):
    spec = importlib.util.spec_from_file_location("_binset", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "TITLE", path.stem), getattr(mod, "PROBLEMS")


def _render_figure(problem, stem: str) -> bool:
    """Render the figure an embedded revision problem needs (binary problems are
    pure text). Returns True if a figure was written."""
    if isinstance(problem, _BoolProblem) and problem.kind in ("diagram", "circuit"):
        _render_circuit(problem.expr, stem)  # pdf + png + svg
        return True
    if isinstance(problem, _FlowProblem):
        _render_flow(problem.algo, stem)
        return True
    return False


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate binary-numbers practice PDFs")
    ap.add_argument("set", type=Path, help="path to a worksheet .py module")
    ap.add_argument("--out", type=Path, default=Path("build"), help="output dir")
    ap.add_argument("--no-pdf", action="store_true", help="emit .tex but skip Tectonic")
    args = ap.parse_args(argv)

    title, problems = _load(args.set)
    name = args.set.stem
    outdir = args.out / name
    figs = outdir / "figs"
    figs.mkdir(parents=True, exist_ok=True)
    for stale in figs.glob("p*.*"):  # drop figures from removed problems
        stale.unlink()

    rendered = []  # (problem, fig_stem | None)
    for i, p in enumerate(problems, 1):
        has_fig = _render_figure(p, str(figs / f"p{i:02d}"))
        rendered.append((p, f"figs/p{i:02d}" if has_fig else None))

    for suffix, key in (("", False), ("-answers", True)):
        tex = latex.build_document(rendered, title=title, answer_key=key)
        tex_path = outdir / f"{name}{suffix}.tex"
        tex_path.write_text(tex)
        print(f"wrote {tex_path}")
        if not args.no_pdf:
            wsbase.compile_tex(tex_path)
            print(f"compiled {tex_path.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
