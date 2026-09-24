"""The starter archive: one spec, three outputs.

A terminal worksheet is only as good as the folder the student is standing in,
so the archive is authored **once** here as a tree of `D` / `F` / `IMG` nodes.
From that one tree the generator derives, so they can never disagree:

- the real folder on disk, zipped into the hand-out `cs17-archive.zip`
- the ASCII tree printed on the worksheet ("what is inside")
- every number in the answer key (`wc -l`, how many lines match `grep`, how
  many `.jpg` files a wildcard picks up) - computed from the same content the
  student's machine will hold.

Query helpers (`nlines`, `ngrep`, `match`, ...) take the archive-relative path,
i.e. `logs/experiment-log-week-01.txt`, without the `cs17-archive/` prefix.
"""

from __future__ import annotations

import zipfile
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path


# ---- the three node kinds ----------------------------------------------------

@dataclass
class File:
    name: str
    body: str                      # full text, newline-terminated


@dataclass
class Image:
    name: str
    size: tuple                    # (width, height) in pixels
    colour: str                    # "#rrggbb" fill
    label: str                     # drawn on the tile so the file looks real


@dataclass
class Dir:
    name: str
    children: list = field(default_factory=list)


def D(name: str, children=None) -> Dir:
    return Dir(name, list(children or []))


def F(name: str, lines) -> File:
    """A text file. `lines` is a list of lines (no trailing newlines) or a str."""
    body = "\n".join(lines) + "\n" if isinstance(lines, (list, tuple)) else lines
    return File(name, body)


def IMG(name: str, *, size=(640, 480), colour="#3b6ea5", label: str = "") -> Image:
    """A real image file (JPEG or PNG, picked from the extension). Sizes differ
    on purpose so `ls -l` shows visibly different byte counts."""
    return Image(name, size, colour, label or Path(name).stem)


# ---- walking / querying ------------------------------------------------------

def walk(root: Dir):
    """Yield (archive-relative path, node) for every node below `root`."""
    def rec(node, prefix):
        for child in node.children:
            path = f"{prefix}{child.name}"
            yield path, child
            if isinstance(child, Dir):
                yield from rec(child, path + "/")
    yield from rec(root, "")


def find(root: Dir, path: str):
    """The node at an archive-relative path, or None."""
    node = root
    for part in path.strip("/").split("/"):
        if not isinstance(node, Dir):
            return None
        node = next((c for c in node.children if c.name == part), None)
        if node is None:
            return None
    return node


def match(root: Dir, pattern: str) -> list:
    """Archive-relative paths matching a glob, e.g. `logs/*.txt`. Matching is on
    the whole relative path, so `*` does not cross a `/` - same as the shell."""
    out = []
    for path, node in walk(root):
        if isinstance(node, Dir):
            continue
        head, _, tail = path.rpartition("/")
        pat_head, _, pat_tail = pattern.rpartition("/")
        if head == pat_head and fnmatch(tail, pat_tail):
            out.append(path)
    return sorted(out)


def text(root: Dir, path: str) -> str:
    node = find(root, path)
    if not isinstance(node, File):
        raise KeyError(f"{path} is not a text file in the archive")
    return node.body


def nlines(root: Dir, pattern: str) -> int:
    """Total line count, as `wc -l` would report it, over every match."""
    return sum(text(root, p).count("\n") for p in match(root, pattern))


def ngrep(root: Dir, pattern: str, word: str) -> int:
    """Lines containing `word` across every match - case sensitive, like grep."""
    return sum(1 for p in match(root, pattern)
               for line in text(root, p).splitlines() if word in line)


def grep_lines(root: Dir, pattern: str, word: str) -> list:
    """The matching lines themselves. Several files -> grep prefixes `path:`."""
    hits = match(root, pattern)
    out = []
    for p in hits:
        for line in text(root, p).splitlines():
            if word in line:
                out.append(f"{p}:{line}" if len(hits) > 1 else line)
    return out


def listing(root: Dir, path: str = "") -> list:
    """Child names of a folder, in the order `ls` shows them (sorted)."""
    node = root if path in ("", ".", "/") else find(root, path)
    return sorted(c.name for c in node.children)


# ---- ASCII tree for the worksheet -------------------------------------------

def ascii_tree(root: Dir) -> str:
    """The tree as the lesson plan draws it: `|--` branches, `` `-- `` for last.
    Folders keep a trailing `/` so a student can tell them apart at a glance."""
    lines = [root.name + "/"]

    def rec(node, prefix):
        kids = node.children
        for i, child in enumerate(kids):
            last = i == len(kids) - 1
            stem = "`-- " if last else "|-- "
            name = child.name + ("/" if isinstance(child, Dir) else "")
            lines.append(prefix + stem + name)
            if isinstance(child, Dir):
                rec(child, prefix + ("    " if last else "|   "))

    rec(root, "")
    return "\n".join(lines)


# ---- writing it out ----------------------------------------------------------

def _write_image(node: Image, dest: Path):
    from PIL import Image as PILImage, ImageDraw, ImageFont

    w, h = node.size
    img = PILImage.new("RGB", (w, h), node.colour)
    draw = ImageDraw.Draw(img)
    # a few flat shapes so the tile reads as a picture, not a colour swatch
    draw.rectangle([0, int(h * 0.68), w, h], fill="#f2efe6")
    draw.ellipse([int(w * 0.62), int(h * 0.10), int(w * 0.86), int(h * 0.34)],
                 fill="#ffd966")
    draw.polygon([(int(w * 0.05), int(h * 0.70)), (int(w * 0.32), int(h * 0.26)),
                  (int(w * 0.60), int(h * 0.70))], fill="#2f4858")
    font = ImageFont.load_default(size=max(14, h // 16))
    draw.text((int(w * 0.05), int(h * 0.78)), node.label, fill="#1b1b1b", font=font)
    fmt = "JPEG" if dest.suffix.lower() in (".jpg", ".jpeg") else "PNG"
    img.save(dest, fmt)


def check_case_collisions(root: Dir) -> None:
    """Refuse two names in one folder that differ only in case.

    The hand-out is unzipped on the student's own laptop, and macOS (APFS) and
    Windows are case *insensitive* by default: `Notes.txt` and `notes.txt` in
    the same folder do not both survive the extraction, one silently overwrites
    the other, and the tree printed on the worksheet no longer matches what the
    student sees. So the archive may never rely on case alone to tell two names
    apart. (Case sensitivity is still taught - through command names, options
    and grep, which are case sensitive on every machine.)"""
    def rec(node, prefix):
        seen = {}
        for child in node.children:
            key = child.name.lower()
            if key in seen:
                raise ValueError(
                    f"{prefix}{seen[key]} and {prefix}{child.name} differ only "
                    "in case; they cannot both survive unzipping on macOS or "
                    "Windows")
            seen[key] = child.name
            if isinstance(child, Dir):
                rec(child, f"{prefix}{child.name}/")
    rec(root, f"{root.name}/")


def materialise(root: Dir, dest: Path) -> Path:
    """Write the archive under `dest`, returning the created top folder."""
    check_case_collisions(root)
    top = dest / root.name
    if top.exists():
        import shutil
        shutil.rmtree(top)

    def rec(node, here: Path):
        here.mkdir(parents=True, exist_ok=True)
        for child in node.children:
            if isinstance(child, Dir):
                rec(child, here / child.name)
            elif isinstance(child, File):
                (here / child.name).write_text(child.body)
            else:
                _write_image(child, here / child.name)

    rec(root, top)
    return top


def make_zip(root: Dir, out_zip: Path, workdir: Path) -> Path:
    """Build the hand-out archive. Files are added in tree order and with fixed
    timestamps so rebuilding the worksheet does not churn the zip."""
    top = materialise(root, workdir)
    out_zip.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED) as z:
        for path in sorted(p for p in top.rglob("*")):
            arc = f"{root.name}/{path.relative_to(top).as_posix()}"
            info = zipfile.ZipInfo(arc + ("/" if path.is_dir() else ""),
                                   date_time=(2026, 1, 1, 0, 0, 0))
            if path.is_dir():
                info.external_attr = (0o40755 << 16) | 0x10
                z.writestr(info, b"")
            else:
                info.external_attr = 0o644 << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                z.writestr(info, path.read_bytes())
    return out_zip
