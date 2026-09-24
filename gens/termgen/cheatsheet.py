"""A one-page cheat sheet, rendered as HTML and printed by headless Chrome.

The worksheet teaches; this is the card the student keeps beside the keyboard.
Every entry shows the same three things, because a command list without them is
the thing students complain about:

    the command       what it does
    $ a real example
    what it printed   and what each part of that output means

The examples all run inside `cs17-archive`, the folder the student already has,
so any line here can be typed straight into the terminal and checked. The
outputs are real: they were captured from Ubuntu 24.04 (bash, GNU coreutils),
the platform the students use.

`FIELDS` draws the pointer block under an output line. It finds the columns by
splitting the real output, so the arrows cannot drift out of alignment with the
text they point at - the same authored-once rule the rest of the generator uses.

LaTeX is not involved. A cheat sheet is a dense two-column card, which CSS does
in a few lines and TeX does not, so this one goes through Chrome instead.
"""

from __future__ import annotations

import html
import re
import shutil
import subprocess
from dataclasses import dataclass, field
from pathlib import Path


CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
]


# ---- the pieces a card is made of --------------------------------------------

@dataclass
class Entry:
    cmd: str                   # the command, as you would type it
    what: str                  # one line: what it does
    ex: str = ""               # a transcript: `$ ...` lines are commands
    ann: str = ""              # pointer block, aligned under the last ex line
    note: str = ""             # the catch, or the reason it matters
    rows: list = field(default_factory=list)   # (key, meaning) reference rows
    box: bool = False          # draw it as a standing rule, not an entry


@dataclass
class Section:
    title: str
    entries: list = field(default_factory=list)
    intro: str = ""


def ENTRY(cmd: str, what: str, *, ex: str = "", ann: str = "",
          note: str = "", rows: list | None = None, box: bool = False) -> Entry:
    """One card. `rows` renders a small (key, meaning) table instead of an
    example - for the things that are keystrokes or symbols rather than
    commands. `box` draws the entry as a standing rule (the safety notes)."""
    return Entry(cmd=cmd, what=what, ex=ex, ann=ann, note=note,
                 rows=rows or [], box=box)


def SECTION(title: str, entries: list, *, intro: str = "") -> Section:
    return Section(title=title, entries=entries, intro=intro)


def FIELDS(line: str, labels: dict) -> str:
    """The pointer block under an output line.

    `labels` maps a whitespace-separated field index of `line` to its label.
    The columns come from the line itself, so an arrow always sits under the
    thing it names. Labels are left-aligned with each other, past the last
    pointer, so the block reads as a legend rather than a staircase.

        >>> print(FIELDS("  3  37 194 notes.txt", {0: "lines", 2: "characters"}))
          |       |
          |       `-- characters
          `---------- lines
    """
    cols, i = [], 0
    for idx, token in enumerate(line.split()):
        i = line.index(token, i)
        if idx in labels:
            cols.append((i, labels[idx]))
        i += len(token)
    cols.sort()
    if not cols:
        return ""
    label_at = max(c for c, _ in cols) + 3

    def row(cells: list) -> str:
        out = ""
        for col, text in cells:
            out += " " * (col - len(out)) + text
        return out

    lines = [row([(c, "|") for c, _ in cols])]
    for n in range(len(cols) - 1, -1, -1):
        col, label = cols[n]
        arrow = "`" + "-" * (label_at - col - 2) + " " + label
        lines.append(row([(c, "|") for c, _ in cols[:n]] + [(col, arrow)]))
    return "\n".join(lines)


# ---- HTML --------------------------------------------------------------------

_CSS = """
/* ---- frappe-ui design tokens -------------------------------------------
   The card is styled with frappe-ui's semantic tokens and type scale so it
   sits next to the rest of the Frappe-flavoured material. This is a plain
   printed page, not a Vue app, so there is no Tailwind preset to pull from:
   the light-mode values below are resolved from frappe-ui's own
   tailwind/generated/{colors,typography,radius}.json (1.0.0-beta.21) and
   declared here as custom properties under their token names.

   Two deliberate departures, both because a printed reference is not an app
   screen:
   - frappe-ui ships no monospace token (its scale is Inter only), so command
     text uses Geist Mono, the same face the CS17 worksheets use, sized to the
     11px text-2xs step.
   - "Gray everywhere, except where colour encodes meaning" is followed to the
     letter: headings, commands and output are all gray. Amber is used only on
     the caution boxes and red only on the one irreversible warning (rm).
   ------------------------------------------------------------------------ */
:root {
  /* text */
  --ink-gray-9: #0f0f0f;  --ink-gray-8: #171717;  --ink-gray-7: #383838;
  --ink-gray-6: #525252;  --ink-gray-5: #7c7c7c;  --ink-gray-4: #999999;
  --ink-amber-8: #bb6f0c; --ink-red-6: #e03434;
  /* backgrounds */
  --surface-base: #ffffff; --surface-gray-1: #f8f8f8; --surface-gray-2: #f3f3f3;
  --surface-amber-1: #fdf8ed;
  /* borders */
  --outline-gray-1: #ededed; --outline-gray-2: #e2e2e2;
  --outline-gray-3: #c7c7c7; --outline-amber-2: #f6eac0;
  /* radius */
  --radius-1: 4px; --radius-4: 8px; --radius-5: 10px;
  /* weight */
  --fw-regular: 420; --fw-medium: 500; --fw-semibold: 600; --fw-bold: 700;
}
@page { size: A4 portrait; margin: 8mm; }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
/* frappe-ui's scale is tuned for a 14px screen. Every size below is the token
   value, unaltered, and the whole card is then rendered at one reduction so it
   fits two sides of A4 - the same type system seen at 84%, rather than a pile
   of one-off sizes that no longer match any step on the scale. */
body { zoom: 0.84; }
body {
  margin: 0; background: var(--surface-base); color: var(--ink-gray-9);
  font-family: "Inter Variable", Inter, "Helvetica Neue", Helvetica, sans-serif;
  /* text-p-2xs: 11px / 1.6 / 0.01em - the card is mostly helper text, which
     wraps, so the loose paragraph scale is the right default */
  font-size: 11px; line-height: 1.6; letter-spacing: 0.01em;
  font-weight: var(--fw-regular);
}
code, pre, .cmd { font-family: "Geist Mono", "SF Mono", Menlo, monospace; }

/* header -------------------------------------------------------------- */
header { display: flex; align-items: baseline; gap: 8px;
         border-bottom: 1px solid var(--outline-gray-2);
         padding-bottom: 6px; margin-bottom: 9px; }
header .mark { font-family: "Geist Mono", monospace; font-size: 18px;
               font-weight: var(--fw-bold); letter-spacing: -0.02em;
               color: var(--ink-gray-5); }
/* text-2xl: 18px / 1.15 */
header h1 { margin: 0; font-size: 18px; line-height: 1.15;
            letter-spacing: 0.01em; font-weight: var(--fw-semibold);
            color: var(--ink-gray-9); }
/* text-p-2xs: 11px / 1.6 */
header .sub { margin-left: auto; font-size: 11px; line-height: 1.6;
              color: var(--ink-gray-5); text-align: right; }

/* columns -------------------------------------------------------------- */
.cols { column-count: 2; column-gap: 6mm; }
section { margin: 0 0 9px; }
/* text-sm: 13px / 1.15. Sentence case: frappe UIs never shout a heading, so a
   section is marked by weight and colour, not by capitals. */
h2 { margin: 0 0 5px; padding-bottom: 3px; font-size: 13px; line-height: 1.15;
     letter-spacing: 0.02em; font-weight: var(--fw-semibold);
     color: var(--ink-gray-5); border-bottom: 1px solid var(--outline-gray-1); }
/* text-p-xs: 12px / 1.6 - a lead paragraph */
.intro { font-size: 12px; line-height: 1.6; color: var(--ink-gray-6);
         margin: 0 0 6px; break-inside: avoid; }
.lead { break-inside: avoid; }
.entry { break-inside: avoid; margin: 0 0 7px; }
.head { display: flex; gap: 7px; align-items: baseline; }
/* text-sm, mono */
.cmd { font-size: 13px; line-height: 1.15; letter-spacing: 0;
       font-weight: var(--fw-semibold); color: var(--ink-gray-9);
       white-space: pre; }
/* text-xs: 12px / 1.15 - a one-line label, so the tight scale */
.what { font-size: 12px; line-height: 1.15; letter-spacing: 0.02em;
        color: var(--ink-gray-6); }

/* transcript ----------------------------------------------------------- */
/* text-2xs step (11px), the smallest on the scale, at the mono face */
pre.ex { margin: 3px 0 0; padding: 5px 7px; white-space: pre; overflow: hidden;
         background: var(--surface-gray-1);
         border: 1px solid var(--outline-gray-2);
         border-radius: var(--radius-4);
         font-size: 11px; line-height: 1.45; letter-spacing: 0;
         color: var(--ink-gray-7); }
pre.ex .p { color: var(--ink-gray-4); }                    /* the $ prompt */
pre.ex .c { color: var(--ink-gray-9); font-weight: var(--fw-medium); }
pre.ex .ann { color: var(--ink-gray-5); }                  /* the legend */
.note { color: var(--ink-gray-6); margin-top: 3px; }
.note b, .intro b, .what b { color: var(--ink-gray-9);
                             font-weight: var(--fw-semibold); }
.note .danger { color: var(--ink-red-6); font-weight: var(--fw-semibold); }

/* key / message reference rows ----------------------------------------- */
table.k { width: 100%; border-collapse: collapse; }
table.k td { border-top: 1px solid var(--outline-gray-1);
             padding: 3px 4px 3px 0; vertical-align: top;
             color: var(--ink-gray-6); }
table.k tr:first-child td { border-top: 0; }
table.k td.k { font-family: "Geist Mono", monospace; font-size: 11px;
               line-height: 1.15; letter-spacing: 0; color: var(--ink-gray-9);
               font-weight: var(--fw-medium);
               white-space: nowrap; width: 1%; padding-right: 10px; }
table.k td b { color: var(--ink-gray-9); font-weight: var(--fw-semibold); }

/* caution box: amber is the one place colour carries meaning ------------ */
.rule { break-inside: avoid; padding: 6px 8px;
        background: var(--surface-amber-1);
        border: 1px solid var(--outline-amber-2);
        border-radius: var(--radius-4); }
.rule .note { color: var(--ink-gray-7); margin-top: 0; }
.rule .note b:first-child { color: var(--ink-amber-8); }

footer { position: fixed; bottom: 0; left: 0; right: 0; font-size: 11px;
         color: var(--ink-gray-4); display: flex;
         justify-content: space-between; }
"""


def _esc(s) -> str:
    return html.escape(str(s), quote=False)


def _transcript(ex: str, ann: str) -> str:
    """One example block. `$ ` lines are what you type, the rest is what came
    back, and the pointer block (if any) hangs under the final output line."""
    out = []
    for line in ex.rstrip("\n").split("\n"):
        if line.startswith("$ "):
            out.append('<span class="p">$</span> <span class="c">%s</span>'
                       % _esc(line[2:]))
        else:
            out.append(_esc(line))
    if ann:
        out.append('<span class="ann">%s</span>' % _esc(ann.rstrip("\n")))
    return '<pre class="ex">%s</pre>' % "\n".join(out)


def _entry(e: Entry) -> str:
    cls = "entry rule" if e.box else "entry"
    out = ['<div class="%s">' % cls]
    if e.cmd or e.what:
        out.append('<div class="head"><span class="cmd">%s</span>'
                   '<span class="what">%s</span></div>'
                   % (_esc(e.cmd), _esc(e.what)))
    if e.ex:
        out.append(_transcript(e.ex, e.ann))
    if e.rows:
        out.append('<table class="k">%s</table>' % "".join(
            "<tr><td class='k'>%s</td><td>%s</td></tr>" % (_esc(k), v)
            for k, v in e.rows))
    if e.note:
        out.append('<div class="note">%s</div>' % e.note)
    out.append("</div>")
    return "".join(out)


def _section(s: Section) -> str:
    """The heading, the intro and the first entry ship as one unbreakable
    `.lead` box; the rest of the entries flow freely, so a long section may
    still split across the column break."""
    lead = ['<div class="lead"><h2>%s</h2>' % _esc(s.title)]
    if s.intro:
        lead.append('<div class="intro">%s</div>' % s.intro)
    entries = list(s.entries)
    if entries:
        lead.append(_entry(entries.pop(0)))
    lead.append("</div>")
    return ("<section>" + "".join(lead)
            + "".join(_entry(e) for e in entries) + "</section>")


# One column is 94mm wide; at the 11px mono step that is 52 characters before a
# transcript line runs under `overflow: hidden` and loses its tail without a
# word of complaint. Checked at build time rather than discovered on paper.
MAX_COLS = 52


def overlong(sections) -> list:
    """(command, line) for every transcript line too wide for the column."""
    out = []
    for section in sections:
        for e in section.entries:
            for block in (e.ex, e.ann):
                for line in block.split("\n"):
                    if len(line) > MAX_COLS:
                        out.append((e.cmd or section.title, line))
    return out


def build_html(sections, *, title: str, subtitle: str = "",
               footer: str = "") -> str:
    """`subtitle` and `footer` are both optional. The card is a reference that
    stands on its own, so it does not carry the name of the worksheet it was
    authored beside."""
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>%s</title><style>%s</style></head><body>"
        "<header><span class='mark'>CS17</span><h1>%s</h1>%s</header>"
        "<div class='cols'>%s</div>"
        "<footer><span>cs17.org</span><span>%s</span></footer>"
        "</body></html>"
        % (_esc(title), _CSS, _esc(title),
           ("<span class='sub'>%s</span>" % subtitle) if subtitle else "",
           "".join(_section(s) for s in sections), _esc(footer)))


# ---- printing ----------------------------------------------------------------

def find_chrome() -> str | None:
    for c in CHROME_CANDIDATES:
        if "/" in c and Path(c).exists():
            return c
        found = shutil.which(c)
        if found:
            return found
    return None


def page_count(pdf_path: Path) -> int:
    return len(re.findall(rb"/Type\s*/Page[^s]", pdf_path.read_bytes()))


def print_pdf(html_path: Path, pdf_path: Path, chrome: str) -> None:
    """Headless Chrome prints the page. `--no-pdf-header-footer` drops the
    browser's own URL/date furniture, which a hand-out must not carry."""
    subprocess.run([
        chrome, "--headless", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=4000",
        f"--print-to-pdf={pdf_path}", html_path.resolve().as_uri(),
    ], check=True, capture_output=True)
