"""CLI: turn an exam-paper module into a question-paper PDF.

Usage:
    python -m gens.examgen.build exams/q1_final/theory.py --out exams/q1_final/build

The module defines TITLE, SUBJECT, PAPER, DURATION, MAX_MARKS, INSTRUCTIONS
and a list PARTS (see gens/examgen/question.py). Flowchart questions have their
charts rendered to build/<name>/figs/ first. No answer key is produced -- an
exam paper ships on its own.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from .. import wsbase
from ..boolgen.diagram import render as render_circuit
from ..flowgen.flowchart import render
from . import latex


def _load(path: Path):
    spec = importlib.util.spec_from_file_location("_exampaper", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _figures(parts, figs_dir: Path) -> dict:
    """Render a flowchart for every question that shows one, keyed by question
    number (which is what the LaTeX side asks for)."""
    figs_dir.mkdir(parents=True, exist_ok=True)
    for stale in figs_dir.glob("q*.*"):  # drop figures from removed questions
        stale.unlink()
    out = {}
    num = 0
    for part in parts:
        for q in part.questions:
            num += 1
            algo, expr = q.figure_algo, q.figure_expr
            if algo is not None:
                # tighter than the worksheets: an exam chart shares its page
                # with a trace table or an answer block, so it gets scaled down
                # -- smaller gaps mean the labels survive that scaling
                render(algo, str(figs_dir / f"q{num:02d}"),  # pdf + png + svg
                       nodesep="0.3", ranksep="0.16")
            elif expr is not None:
                render_circuit(expr, str(figs_dir / f"q{num:02d}"))
            else:
                continue
            out[num] = f"figs/q{num:02d}.pdf"
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate an exam question paper PDF")
    ap.add_argument("paper", type=Path, help="path to an exam paper .py module")
    ap.add_argument("--out", type=Path, default=Path("build"), help="output dir")
    ap.add_argument("--no-pdf", action="store_true", help="emit .tex but skip Tectonic")
    args = ap.parse_args(argv)

    mod = _load(args.paper)
    name = args.paper.stem
    outdir = args.out / name
    outdir.mkdir(parents=True, exist_ok=True)

    parts = getattr(mod, "PARTS", [])
    figs = _figures(parts, outdir / "figs")
    if figs:
        print(f"rendered {len(figs)} flowcharts -> {outdir / 'figs'}")

    tex = latex.build_document(
        parts,
        title=mod.TITLE,
        subject=mod.SUBJECT,
        paper=getattr(mod, "PAPER", ""),
        duration=mod.DURATION,
        max_marks=getattr(mod, "MAX_MARKS", None),
        instructions=getattr(mod, "INSTRUCTIONS", ()),
        date=getattr(mod, "DATE", None),
        figs=figs,
    )
    tex_path = outdir / f"{name}.tex"
    tex_path.write_text(tex)
    print(f"wrote {tex_path}")
    if not args.no_pdf:
        wsbase.compile_tex(tex_path)
        print(f"compiled {tex_path.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
