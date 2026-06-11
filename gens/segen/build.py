"""CLI: turn a seven-segment worksheet module into worksheet + answer-key PDFs.

Usage:
    python -m gens.segen.build sevenseg_worksheet.py
    python -m gens.segen.build sevenseg_worksheet.py --out build --no-pdf

The module defines TITLE and a list PROBLEMS. Everything is drawn inline with
TikZ (no external figures), so this just emits the .tex and compiles it.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from .. import wsbase
from . import latex


def _load(path: Path):
    spec = importlib.util.spec_from_file_location("_segset", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return getattr(mod, "TITLE", path.stem), getattr(mod, "PROBLEMS")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate seven-segment practice PDFs")
    ap.add_argument("set", type=Path, help="path to a worksheet .py module")
    ap.add_argument("--out", type=Path, default=Path("build"), help="output dir")
    ap.add_argument("--no-pdf", action="store_true", help="emit .tex but skip Tectonic")
    args = ap.parse_args(argv)

    title, problems = _load(args.set)
    name = args.set.stem
    outdir = args.out / name
    outdir.mkdir(parents=True, exist_ok=True)

    for suffix, key in (("", False), ("-answers", True)):
        tex = latex.build_document(problems, title=title, answer_key=key)
        tex_path = outdir / f"{name}{suffix}.tex"
        tex_path.write_text(tex)
        print(f"wrote {tex_path}")
        if not args.no_pdf:
            wsbase.compile_tex(tex_path)
            print(f"compiled {tex_path.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
