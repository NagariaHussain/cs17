"""Render the same worksheet as Markdown, for publishing on the wiki.

The PDF is the printed hand-out. The Markdown is the same assignment as a web
page, built from the same PARTS so the two cannot drift apart.

Two things change between the formats, and only two:

- **Ruled answer lines disappear.** They are a paper device. The web version
  tells the student to keep answers in their own document instead, which is why
  `build_document` takes the answer note as an argument rather than baking it
  into the shared LEAD.
- **Author prose is translated, not re-written.** The part intros, notes and
  captions are authored once as LaTeX (they carry `\\cmd{...}`, `\\emph{...}`,
  boxes and lists on purpose). `_md` converts exactly the macros this generator
  uses and raises on anything it does not recognise, so a new macro fails the
  build instead of leaking `\\cmd{` onto the wiki.
"""

from __future__ import annotations

import re
import textwrap

from . import tree as T
from .task import Task, PathTable, ErrorTable, Predict, Box, Part


# ---- LaTeX prose -> Markdown -------------------------------------------------

def _arg(s: str, i: int) -> tuple:
    """Read a brace-delimited argument starting at s[i] == '{'. Returns
    (contents, index just past the closing brace)."""
    depth, j = 0, i
    while j < len(s):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1
    raise ValueError(f"unbalanced braces in author prose: {s[i:i + 60]!r}")


_CODE = ("cmd", "texttt")
_EMPH = (("emph", "*%s*"), ("textbf", "**%s**"), ("textit", "*%s*"))


def _wrappers(s: str, codes: list) -> str:
    """Convert the inline macros, innermost first so nesting resolves.

    A code span is stashed behind a placeholder and put back at the very end.
    Its contents are a literal command and must survive every text-level rule
    that follows - above all `~`, which is a hard space in LaTeX prose but a
    home folder inside \cmd{~/Desktop/...}."""
    for name in _CODE:
        pat = "\\" + name + "{"
        while (i := s.find(pat)) != -1:
            body, end = _arg(s, i + len(pat) - 1)
            codes.append(body)
            s = s[:i] + f"@CODE{len(codes) - 1}@" + s[end:]
    for name, fmt in _EMPH:
        pat = "\\" + name + "{"
        while (i := s.find(pat)) != -1:
            body, end = _arg(s, i + len(pat) - 1)
            s = s[:i] + fmt % _wrappers(body, codes) + s[end:]
    return s


def _indent(block: str, pad: str) -> str:
    """Indent every line of a block except the first, leaving blanks blank.
    Markdown needs this for anything that follows the first paragraph of a list
    item - a second paragraph at column 0 ends the list instead of joining it."""
    first, *rest = block.split("\n")
    return "\n".join([first] + [pad + ln if ln.strip() else "" for ln in rest])


def _lists(s: str) -> str:
    """itemize -> `- `, enumerate -> `1. ` (Markdown renumbers by itself)."""
    for env, bullet in (("itemize", "- "), ("enumerate", "1. ")):
        while (i := s.find(r"\begin{%s}" % env)) != -1:
            j = s.index(r"\end{%s}" % env)
            body = s[i + len(r"\begin{%s}" % env):j]
            items = [x.strip() for x in body.split(r"\item") if x.strip()]
            pad = " " * len(bullet)
            s = (s[:i] + "\n\n"
                 + "\n".join(bullet + _indent(x, pad) for x in items) + "\n\n"
                 + s[j + len(r"\end{%s}" % env):])
    return s


def _md(text: str) -> str:
    """One author-prose string, as Markdown."""
    if not text:
        return ""
    s, codes = text, []
    s = s.replace(r"\subsection*{Hand in}", "")          # the renderer adds it
    # boxes: an \fbox'd minipage is an aside -> a blockquote, marked for later
    s = re.sub(r"\\noindent\\fbox\{\\begin\{minipage\}\{[^}]*\}", "@QUOTE@", s)
    s = re.sub(r"\\fbox\{\\begin\{minipage\}\{[^}]*\}", "@QUOTE@", s)
    s = s.replace(r"\end{minipage}}", "@ENDQUOTE@")
    # paragraph breaks and spacing
    s = re.sub(r"\\par\\vspace\{[^}]*\}", "\n\n", s)
    s = re.sub(r"\\vspace\*?\{[^}]*\}", "", s)
    s = re.sub(r"\\hspace\*?\{[^}]*\}", "", s)
    s = re.sub(r"\\\\\[[^\]]*\]", "\n", s)
    s = s.replace(r"\par", "\n\n").replace(r"\quad", " ")
    s = s.replace(r"$\rightarrow$", "→")
    s = _wrappers(s, codes)
    s = _lists(s)
    # font switches carry no meaning on the web
    for macro in (r"\noindent", r"\small", r"\footnotesize", r"\itshape",
                  r"\centering", r"\bfseries"):
        s = s.replace(macro, "")
    s = s.replace("~", " ")                               # LaTeX hard space
    for esc, ch in ((r"\&", "&"), (r"\%", "%"), (r"\_", "_"), (r"\#", "#"),
                    (r"\$", "$")):
        s = s.replace(esc, ch)
    s = s.replace("{", "").replace("}", "")
    s = s.replace("@QUOTE@", "\n\n@QUOTE@").replace("@ENDQUOTE@", "@ENDQUOTE@\n\n")
    if "\\" in s:
        leftover = re.search(r"\\[A-Za-z*]+", s)
        raise ValueError(
            "markdown renderer met a LaTeX macro it does not handle: "
            f"{leftover.group(0) if leftover else s[:60]!r}. Add it to "
            "gens/termgen/markdown.py rather than letting it reach the wiki.")
    # tidy the double spaces that removed macros leave behind, but never touch
    # the leading whitespace - that is list indentation and Markdown reads it
    def tidy(line: str) -> str:
        lead = line[:len(line) - len(line.lstrip())]
        return (lead + re.sub(r"[ \t]+", " ", line.lstrip())).rstrip()

    s = "\n".join(tidy(ln) for ln in s.split("\n"))
    s = re.sub(r"\n{3,}", "\n\n", s)
    # code spans go back in last, untouched by every rule above
    s = re.sub(r"@CODE(\d+)@", lambda m: "`%s`" % codes[int(m.group(1))], s)
    return s.strip()


def _quote(s: str) -> str:
    """Turn the @QUOTE@ markers into real blockquotes."""
    out, buf, quoting = [], [], False

    def flush():
        while buf and not buf[-1].strip():          # no dangling "> " line
            buf.pop()
        out.extend("> " + ln if ln.strip() else ">" for ln in buf)
        buf.clear()

    for line in s.split("\n"):
        if "@QUOTE@" in line:
            quoting = True
            line = line.replace("@QUOTE@", "").strip()
            if not line:
                continue
        if "@ENDQUOTE@" in line:
            line = line.replace("@ENDQUOTE@", "").strip()
            if line:
                buf.append(line)
            flush()
            quoting = False
            continue
        (buf if quoting else out).append(line)
    flush()
    return "\n".join(out)


def _prose(text: str) -> str:
    return _quote(_md(text))


# ---- small pieces ------------------------------------------------------------

def _cell(v) -> str:
    """A literal path or command in a table cell. A pipe would end the column."""
    return "`%s`" % str(v).replace("|", "\\|") if v else ""


_FENCE_COLS = 86        # a fenced block does not wrap; past this it scrolls


def _fence(body: str, indent: str = "", wrap: bool = False) -> str:
    """A fenced block. `wrap` folds prose (the answer key's expected output) so
    a wiki page does not scroll sideways. Commands are never wrapped, since a
    folded command is not one you can retype."""
    src = []
    for line in body.rstrip("\n").split("\n"):
        if wrap and len(line) > _FENCE_COLS:
            src += textwrap.wrap(line, _FENCE_COLS, break_long_words=False,
                                 break_on_hyphens=False)
        else:
            src.append(line)
    return "\n".join(indent + ln for ln in ["```text", *src, "```"])


def _table(headers: list, rows: list) -> str:
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(out)


# ---- the write-in drills -----------------------------------------------------

def _path_table(t: PathTable, *, answer: bool) -> str:
    headers = (["You are in", "You want to reach", "Relative path",
                "Absolute path"] if t.absolute else
               ["You are in", "You want to reach", "Command to type"])
    rows = []
    for here, target, *answers in t.rows:
        rows.append([_cell(here), _cell(target)]
                    + [(_cell(a) if answer else "") for a in answers])
    return _prose(t.caption) + "\n\n" + _table(headers, rows)


def _error_table(t: ErrorTable, *, answer: bool) -> str:
    rows = [[_cell(broken),
             _cell(err) if answer else "",
             (why if answer else "")]
            for broken, err, why in t.rows]
    return (_prose(t.caption) + "\n\n"
            + _table(["Run this", "What the shell printed", "Why it failed"], rows))


def _predict_table(t: Predict, *, answer: bool) -> str:
    rows = [[_cell(c), (out if answer else "")] for c, out in t.rows]
    return (_prose(t.caption) + "\n\n"
            + _table(["Command", "Write your prediction, then run the line"], rows))


def _box(b: Box, *, answer: bool) -> str:
    """The web has no paper to write on, so the blank becomes an instruction.
    On the key it becomes the thing itself, in a fenced block."""
    if answer:
        return _prose(b.prompt) + "\n\n" + _fence(b.answer)
    return _prose(b.prompt)


# ---- one part ----------------------------------------------------------------

def _task(n: int, t: Task, *, answer: bool) -> str:
    pad = " " * len(f"{n}. ")
    out = [f"{n}. " + _indent(_prose(t.text), pad)]
    if t.hint:
        out.append(pad + "*Hint: %s*" % _prose(t.hint))
    if t.given:
        out.append(_fence(t.given, pad))
    if answer:
        if t.cmd:
            out.append(_fence(t.cmd, pad))
        if t.expect:
            out.append(pad + "**Expected:**")
            out.append(_fence(t.expect, pad, wrap=True))
    return "\n\n".join(out)


def _part(idx: int, p: Part, *, answer: bool) -> str:
    lesson = p.lesson + (" (not taught yet)" if p.bonus else "")
    out = [f"## Part {idx}. {p.title}"]
    if lesson:
        out.append(f"*{lesson}*")
    if p.intro:
        out.append(_prose(p.intro))
    if p.recap:
        out.append(_table(["Command", "What it does"],
                          [[_cell(c), m] for c, m in p.recap]))
    n = 0
    for item in p.tasks:
        if isinstance(item, Task):
            n += 1
            out.append(_task(n, item, answer=answer))
        elif isinstance(item, PathTable):
            out.append(_path_table(item, answer=answer))
        elif isinstance(item, ErrorTable):
            out.append(_error_table(item, answer=answer))
        elif isinstance(item, Predict):
            out.append(_predict_table(item, answer=answer))
        elif isinstance(item, Box):
            out.append(_box(item, answer=answer))
    if p.note:
        out.append("> **Remember**\n>\n" + "\n".join(
            "> " + ln if ln else ">" for ln in _prose(p.note).split("\n")))
    return "\n\n".join(out)


# ---- the document ------------------------------------------------------------

def build_document(parts, *, title: str, archive: T.Dir, zip_name: str,
                   lead: str, answer_key: bool, habits: str = "",
                   answer_note: str = "", reference: list | None = None,
                   closing: str = "") -> str:
    out = [f"# {title}", "*CS17 · cs17.org*"]
    if answer_key:
        out.append("*Answer key: model commands and expected output. Many tasks "
                   "have more than one correct answer. Check that the student "
                   "reached the correct folder and the correct file.*")
    out.append(_prose(lead))
    if answer_note:
        out.append(_prose(answer_note))
    out.append(f"## What is inside `{zip_name}`")
    out.append(f"Task 1 unpacks the zip. You get one folder with the name "
               f"`{archive.name}`, and every file and folder in this "
               f"assignment is inside it. The map of that folder is not "
               f"printed here. It is inside the archive, in `README.txt`, and "
               f"Part 1 asks you to print it and copy it out. Keep your copy "
               f"beside you: most of the work in this assignment is to reach "
               f"the correct place in that tree.")
    if answer_key:
        out.append(_fence(T.ascii_tree(archive)))
    if habits:
        out.append(_prose(habits))
    for i, p in enumerate(parts, 1):
        out.append(_part(i, p, answer=answer_key))
    if closing:
        out.append("## Hand in")
        out.append(_prose(closing))
    if reference:
        out.append("## Command reference")
        out.append(_table(["Command", "Use"],
                          [[_cell(c), u] for c, u in reference]))
    return "\n\n".join(out).rstrip() + "\n"
