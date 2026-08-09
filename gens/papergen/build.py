"""CLI: turn a paper module into the question paper + answer-key PDFs.

Usage:
    python -m gens.papergen.build paper_1_practical.py
    python -m gens.papergen.build paper_1_practical.py --out build --no-pdf

The module defines PAPER (a `Paper`). Everything renders inline — spreadsheet
grids as tabulars, Scratch solutions via scratchgen — so this only emits the
.tex and compiles it with Tectonic.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from .. import wsbase
from . import latex


def _load(path: Path):
    spec = importlib.util.spec_from_file_location("_paper", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate question-paper PDFs")
    ap.add_argument("paper", type=Path, help="path to a paper .py module")
    ap.add_argument("--out", type=Path, default=Path("build"), help="output dir")
    ap.add_argument("--no-pdf", action="store_true", help="emit .tex but skip Tectonic")
    ap.add_argument("--paper-only", action="store_true",
                    help="skip the answer key (e.g. when printing for an exam)")
    args = ap.parse_args(argv)

    mod = _load(args.paper)
    name = args.paper.stem
    paper = mod.PAPER.check()
    outdir = args.out / name
    outdir.mkdir(parents=True, exist_ok=True)

    # unnamed sections (a single-section hand-out) have no name to report, so the
    # breakdown is only worth printing when the sections are actually named
    named = [s for s in paper.sections if s.name]
    breakdown = ("  —  " + ", ".join(f"{s.name} {s.marks}" for s in named)) if named else ""
    print(f"{paper.title}: {paper.marks} marks{breakdown}")

    variants = (("", False),) if args.paper_only else (("", False), ("-answers", True))
    for suffix, key in variants:
        tex = latex.build_document(paper, answer_key=key)
        tex_path = outdir / f"{name}{suffix}.tex"
        tex_path.write_text(tex)
        print(f"wrote {tex_path}")
        if not args.no_pdf:
            wsbase.compile_tex(tex_path)
            print(f"compiled {tex_path.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
