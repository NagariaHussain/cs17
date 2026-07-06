"""CLI: turn a build-along worksheet module into worksheet + answer-key PDFs.

Usage:
    python -m gens.scratchgen.build worksheet_12_scratch_projects.py
    python -m gens.scratchgen.build worksheet_12_scratch_projects.py --out build --no-pdf

The module defines TITLE and a list ACTIVITIES of BUILD(...) projects. Every
script is rendered inline with the scratch3 package (no external figures), so
this just emits the .tex and compiles it with Tectonic.
"""

from __future__ import annotations

import argparse
import importlib.util
from pathlib import Path

from .. import wsbase
from . import latex


def _load(path: Path):
    spec = importlib.util.spec_from_file_location("_scratchset", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate build-along Scratch PDFs")
    ap.add_argument("set", type=Path, help="path to a worksheet .py module")
    ap.add_argument("--out", type=Path, default=Path("build"), help="output dir")
    ap.add_argument("--no-pdf", action="store_true", help="emit .tex but skip Tectonic")
    args = ap.parse_args(argv)

    mod = _load(args.set)
    name = args.set.stem
    title = getattr(mod, "TITLE", name)
    activities = mod.ACTIVITIES
    palette = getattr(mod, "PALETTE", None)
    lead = getattr(mod, "LEAD", None)
    outdir = args.out / name
    outdir.mkdir(parents=True, exist_ok=True)

    for suffix, key in (("", False), ("-answers", True)):
        tex = latex.build_document(activities, title=title, answer_key=key,
                                   palette=palette, lead=lead)
        tex_path = outdir / f"{name}{suffix}.tex"
        tex_path.write_text(tex)
        print(f"wrote {tex_path}")
        if not args.no_pdf:
            wsbase.compile_tex(tex_path)
            print(f"compiled {tex_path.with_suffix('.pdf')}")


if __name__ == "__main__":
    main()
