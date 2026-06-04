"""CLI: turn a flowchart worksheet module into worksheet + answer-key PDFs.

Usage:
    python -m flowgen.build flowchart_worksheet.py
    python -m flowgen.build flowchart_worksheet.py --out build --no-pdf

The module defines TITLE and a list PROBLEMS of TRACE(...)/DRAW(...) problems.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

import wsbase

from . import latex
from .flowchart import render


def _load(path: Path):
    spec = importlib.util.spec_from_file_location("_flowset", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "TITLE", path.stem), getattr(mod, "PROBLEMS")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate flowchart practice PDFs")
    ap.add_argument("set", type=Path, help="path to a worksheet .py module")
    ap.add_argument("--out", type=Path, default=Path("build"), help="output dir")
    ap.add_argument("--no-pdf", action="store_true", help="emit .tex + figures but skip Tectonic")
    args = ap.parse_args(argv)

    title, problems = _load(args.set)
    name = args.set.stem
    figs = args.out / name / "figs"
    figs.mkdir(parents=True, exist_ok=True)
    for stale in figs.glob("p*.*"):  # drop figures from removed problems
        stale.unlink()

    rendered = []
    for i, p in enumerate(problems, 1):
        render(p.algo, str(figs / f"p{i:02d}"))  # pdf + png + svg
        rendered.append((p, f"figs/p{i:02d}"))
    print(f"rendered {len(rendered)} flowcharts -> {figs}")

    for suffix, key in (("", False), ("-answers", True)):
        tex = latex.build_document(rendered, title=title, answer_key=key)
        tex_path = args.out / name / f"{name}{suffix}.tex"
        tex_path.write_text(tex)
        print(f"wrote {tex_path}")
        if not args.no_pdf:
            wsbase.compile_tex(tex_path)
            print(f"compiled {tex_path.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
