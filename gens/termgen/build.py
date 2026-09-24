"""CLI: turn a terminal worksheet module into worksheet + answer key + the zip.

Usage:
    python -m gens.termgen.build worksheet_21_terminal_shell.py
    python -m gens.termgen.build worksheet_21_terminal_shell.py --out build --no-pdf
    python -m gens.termgen.build worksheet_21_terminal_shell.py --no-zip

The module defines TITLE, LEAD, ARCHIVE (the tree students receive) and PARTS.
The zip lands next to the PDFs so the hand-out and the sheet describing it are
always built together from the same source.
"""

from __future__ import annotations

import argparse
import importlib.util
import shutil
from pathlib import Path

from .. import wsbase
from . import cheatsheet, latex, markdown, tree


def _load(path: Path):
    spec = importlib.util.spec_from_file_location("_termset", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main(argv=None):
    ap = argparse.ArgumentParser(description="Generate a terminal & shell worksheet")
    ap.add_argument("set", type=Path, help="path to a worksheet .py module")
    ap.add_argument("--out", type=Path, default=Path("build"), help="output dir")
    ap.add_argument("--no-pdf", action="store_true", help="emit .tex but skip Tectonic")
    ap.add_argument("--no-zip", action="store_true", help="skip the student archive")
    ap.add_argument("--no-md", action="store_true",
                    help="skip the Markdown build (the wiki version)")
    ap.add_argument("--no-cheatsheet", action="store_true",
                    help="skip the one-page cheat sheet (needs Chrome)")
    args = ap.parse_args(argv)

    mod = _load(args.set)
    name = args.set.stem
    archive = mod.ARCHIVE
    zip_name = getattr(mod, "ZIP_NAME", f"{archive.name}.zip")
    outdir = args.out / name
    outdir.mkdir(parents=True, exist_ok=True)

    if not args.no_zip:
        staging = outdir / "_archive"
        zip_path = tree.make_zip(archive, outdir / zip_name, staging)
        shutil.rmtree(staging, ignore_errors=True)   # only the zip ships
        print(f"wrote {zip_path}")

    common = dict(
        title=getattr(mod, "TITLE", name),
        archive=archive,
        zip_name=zip_name,
        lead=getattr(mod, "LEAD", ""),
        habits=getattr(mod, "HABITS", ""),
        reference=getattr(mod, "REFERENCE", None),
        closing=getattr(mod, "CLOSING", ""),
    )

    for suffix, key in (("", False), ("-answers", True)):
        tex = latex.build_document(
            mod.PARTS, answer_key=key,
            answer_note=getattr(mod, "ANSWER_NOTE", ""), **common)
        tex_path = outdir / f"{name}{suffix}.tex"
        tex_path.write_text(tex)
        print(f"wrote {tex_path}")
        if not args.no_pdf:
            wsbase.compile_tex(tex_path)
            print(f"compiled {tex_path.with_suffix('.pdf')}")

        # the same assignment as a web page, for the wiki
        if not args.no_md:
            md = markdown.build_document(
                mod.PARTS, answer_key=key,
                answer_note=getattr(mod, "ANSWER_NOTE_MD", ""), **common)
            md_path = outdir / f"{name}{suffix}.md"
            md_path.write_text(md)
            print(f"wrote {md_path}")

    # the one-page cheat sheet: HTML + headless Chrome, not LaTeX (see
    # gens/termgen/cheatsheet.py). A missing Chrome is a warning, not a build
    # failure - the worksheet and its answer key do not depend on it.
    sheet = getattr(mod, "CHEAT_SHEET", None)
    if sheet and not args.no_cheatsheet:
        html = cheatsheet.build_html(
            sheet,
            title=getattr(mod, "CHEAT_TITLE", "Cheat Sheet"),
            subtitle=getattr(mod, "CHEAT_SUBTITLE", ""),
            footer=getattr(mod, "CHEAT_FOOTER", ""))
        for cmd, line in cheatsheet.overlong(sheet):
            print(f"warning: cheat sheet line is {len(line)} chars, over "
                  f"{cheatsheet.MAX_COLS}, and will be clipped ({cmd}): {line}")
        html_path = outdir / f"{getattr(mod, 'CHEAT_NAME', 'cheat-sheet')}.html"
        html_path.write_text(html)
        print(f"wrote {html_path}")
        chrome = cheatsheet.find_chrome()
        if chrome is None:
            print("warning: no Chrome or Chromium found; cheat sheet PDF skipped")
        else:
            pdf = html_path.with_suffix(".pdf")
            cheatsheet.print_pdf(html_path, pdf, chrome)
            # Two sides of one sheet of paper is the budget. Past that it stops
            # being a card you can keep beside the keyboard, and CSS columns
            # drop what does not fit instead of complaining, so count the pages.
            pages = cheatsheet.page_count(pdf)
            if pages > 2:
                print(f"warning: cheat sheet is {pages} pages; trim it or "
                      "shrink the type in gens/termgen/cheatsheet.py")
            print(f"printed {pdf} ({pages} pages)")


if __name__ == "__main__":
    main()
