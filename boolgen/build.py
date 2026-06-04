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
import subprocess
import sys
from pathlib import Path

from . import latex
from .diagram import render
from .expr import variables
from .problem import Problem, DIAGRAM


def _normalize(item) -> Problem:
    """Accept a Problem, a bare expression (-> DIAGRAM), or (title, expr)."""
    if isinstance(item, Problem):
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
    return title, problems


def _compile(tex_path: Path):
    # run with cwd at the .tex dir so figure paths stay relative & reproducible
    subprocess.run(["tectonic", tex_path.name], cwd=tex_path.parent, check=True)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate Boolean-algebra practice PDFs")
    ap.add_argument("set", type=Path, help="path to a problem-set .py module")
    ap.add_argument("--out", type=Path, default=Path("build"), help="output dir")
    ap.add_argument("--no-pdf", action="store_true", help="emit .tex + figures but skip Tectonic")
    args = ap.parse_args(argv)

    title, problems = _load_set(args.set)
    name = args.set.stem
    figs = args.out / name / "figs"
    figs.mkdir(parents=True, exist_ok=True)
    for stale in figs.glob("p*.*"):  # drop figures from removed problems
        stale.unlink()

    rendered = []  # (Problem, fig_stem | None)
    nfigs = 0
    for i, item in enumerate(problems, 1):
        p = _normalize(item)
        if p.kind == "truthtable" and len(variables(p.expr)) > 3:
            raise ValueError(f"problem {i}: truth-table problems are capped at 3 variables")
        fig = None
        # only kinds that SHOW a circuit need a rendered figure (the diagram
        # problem on the worksheet; the circuit problem on the answer key)
        if p.kind in ("diagram", "circuit"):
            render(p.expr, str(figs / f"p{i:02d}"))  # writes pdf + png + svg
            fig = f"figs/p{i:02d}"
            nfigs += 1
        rendered.append((p, fig))
    print(f"rendered {nfigs} diagrams -> {figs}")

    # two separate PDFs: the worksheet, and the answer key
    for suffix, key in (("", False), ("-answers", True)):
        tex = latex.build_document(rendered, title=title, answer_key=key)
        tex_path = args.out / name / f"{name}{suffix}.tex"
        tex_path.write_text(tex)
        print(f"wrote {tex_path}")
        if not args.no_pdf:
            _compile(tex_path)
            print(f"compiled {tex_path.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
