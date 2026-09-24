# cs17 — practice worksheets & assignment prep

Source for **cs17.org** course materials. Two kinds of material live here:

- **`worksheets/`** — generated, non-graded practice. Each worksheet produces two
  polished PDFs (the worksheet + a separate answer key) plus standalone diagram
  images (PNG/SVG) for reuse elsewhere (slides, web, etc.).
- **`assignments/`** — graded assessment prep: seed-data generators, model
  solutions, and instructor walkthroughs backing each assignment that gets
  hand-published to the wiki. See [`assignments/README.md`](assignments/README.md).

## Repo layout

```
gens/                       shared worksheet-generator engine (the packages below)
  boolgen/  flowgen/  bingen/  segen/  turtlegen/  boxgen/  scratchgen/  examgen/  wsbase.py
  papergen/                 graded question papers (sections + marks), not worksheets
worksheets/
  worksheet1_boolean_algebra/   worksheet_1_boolean_algebra.py            + build/   (WS1)
  worksheet2_flowcharts/        worksheet_2_flowcharts.py                 + build/   (WS2)
  worksheet3_binary/            worksheet_3_binary.py                   + build/   (WS3)
  worksheet4_hexadecimal/       worksheet_4_hexadecimal.py               + build/   (WS4)
  worksheet5_sevensegment/      worksheet_5_seven_segment_display.py     + build/   (WS5)
  worksheet6_decisions/         worksheet_6_decisions_and_calculations.py + build/   (WS6)
  worksheet7_loops/             worksheet_7_simple_loops.py             + build/   (WS7)
  worksheet8_flowcharts_intermediate/ worksheet_8_flowcharts_intermediate.py + build/ (WS8)
  worksheet9_logic_and_flowcharts/ worksheet_9_logic_and_flowcharts.py     + build/   (WS9)
  worksheet10_drawing_flowcharts/ … worksheet18_scratch_dodge/          + build/   (WS10–18)
  worksheet19_scratch_invaders/ worksheet_19_scratch_invaders.py        + build/   (WS19, Scratch G)
  worksheet20_debugging_flowcharts/ worksheet_20_debugging_flowcharts.py + build/  (WS20)
  worksheet21_terminal_shell/   worksheet_21_terminal_shell.py + build/ (WS21, + cs17-archive.zip)
papers/
  paper1_practical/             paper_1_practical.py (Calc + Scratch)      + build/
  paper2_trace/                 paper_2_trace.py (trace a Scratch script)  + build/
exams/
  q1_final/                     theory.py + practical.py (gens.examgen)      + build/
pdfs/                           all PDFs copied in, split into sheets/ and answer_keys/
scratch-dino/                   Chrome-Dino reference build (REFERENCE_GAME.md + sliced assets)
scratch-invaders/               Space-Invaders reference build (REFERENCE_GAME.md + slice_sprite.py + sliced assets)
assignments/
  q1-p2_jugaad_inventory/       README + build_seed.py + references/
```

## The generators (in `gens/`)

- **`gens.boolgen`** — Boolean algebra (logic-gate diagram ↔ expression ↔ truth table).
- **`gens.flowgen`** — flowcharts of simple algorithms (flowchart ↔ pseudocode ↔ trace table).
- **`gens.bingen`** — number bases (binary ↔ decimal ↔ hexadecimal, ASCII codes → message).
- **`gens.segen`** — seven-segment displays; **`gens.turtlegen`** — the coordinate grid;
  **`gens.boxgen`** — sprite anchor points on the grid.
- **`gens.examgen`** — **graded exam question papers** (`exams/`), not worksheets: a
  paper is a list of parts, each part a list of questions (MCQ, short answer,
  Boolean, trace / draw / debug a flowchart). Flowchart questions wrap `flowgen`
  problems and Boolean ones wrap `boolgen` expressions, so an exam question is
  built from the same single source as the practice it came from. **No answer key
  is generated** — an exam paper ships on its own.
- **`gens.termgen`** — **terminal & shell** drills: one authored folder tree becomes
  the `.zip` the student extracts, the map printed on the sheet, and every number in
  the answer key. See the [termgen section](#termgen--terminal--shell-drills) below.
- **`gens.scratchgen`** — follow-along **Scratch build-along** sheets: author each finished
  script once and render it as real Scratch blocks (Scratch A–G, WS12–19). See the
  [scratchgen section](#scratchgen--scratch-build-along-sheets-ag) below.

All share the same idea: author each problem **once** as a single source of
truth, then derive every representation from it so they can't disagree. Build
(each worksheet's PDFs land in its own `build/` folder, and `make` also collects
every PDF into the top-level `pdfs/` folder as symlinks for easy browsing —
`pdfs/sheets/` for the worksheets, `pdfs/answer_keys/` for the answer keys):

```bash
make            # all worksheets, then refresh pdfs/
make boolean    # gens.boolgen -> worksheets/worksheet1_boolean_algebra/build/
make flowchart  # gens.flowgen -> worksheets/worksheet2_flowcharts/build/
make binary     # gens.bingen  -> worksheets/worksheet3_binary/build/        (Worksheet 3)
make hex        # gens.bingen  -> worksheets/worksheet4_hexadecimal/build/   (Worksheet 4)
make mixed      # gens.boolgen -> worksheets/worksheet9_logic_and_flowcharts/build/ (Worksheet 9)
make debugging  # gens.flowgen -> worksheets/worksheet20_debugging_flowcharts/build/ (Worksheet 20)
make terminal   # gens.termgen -> worksheets/worksheet21_terminal_shell/build/       (Worksheet 21 + its zip)
make exams      # gens.examgen -> exams/q1_final/build/{theory,practical}/  (question papers)
make pdfs       # just rebuild pdfs/sheets + pdfs/answer_keys from existing builds
```

Every worksheet (not the answer key) carries a **Name / Date** field under the
title, since the sheets are printed and handed out. It is one shared macro
(`\wsnamefield`, defined in `gens/wsbase.py`) that each generator emits on the
worksheet document only.

---

## boolgen — Boolean algebra

## How it works

Each problem is authored as **one expression** — the single source of truth.
From that one tree the generator derives, so they can never disagree:

- the **gate diagram** (drawn by [`schemdraw`](https://schemdraw.readthedocs.io))
- the **Boolean expression** in engineering notation (overbar / `+` / `·` / `⊕`)
- the **truth table** (computed by evaluating the expression)
- a **simplified form** for the answer key (via sympy — e.g. De Morgan)

Final layout is typeset with **LaTeX via [Tectonic](https://tectonic-typesetting.github.io)**
(self-contained — auto-downloads any packages it needs; no MacTeX install).

```
worksheet_1_boolean_algebra.py ──▶ gens.boolgen ──▶ worksheet1_boolean_algebra/build/worksheet_1_boolean_algebra/
                                   ├── figs/pNN.{pdf,png,svg}  ← reusable diagram images
                                   ├── worksheet_1_boolean_algebra.pdf         ← questions
                                   └── worksheet_1_boolean_algebra-answers.pdf ← answer key (separate)
```

## Four problem types

All authored from the same expression; the *type* picks which direction the
student works:

| In `worksheet_1_boolean_algebra.py`  | Student is given… | …and must produce            |
|----------------------------|-------------------|------------------------------|
| `parse("...")`             | the gate diagram  | the expression + truth table |
| `CIRCUIT(parse("..."))`    | the expression    | the logic-gate circuit       |
| `TRUTHTABLE(parse("..."))` | the expression    | the truth table (≤ 3 vars)   |
| `FROMTABLE(parse("..."))`  | the truth table   | the expression + the circuit (≤ 3 vars) |

`FROMTABLE` runs the loop the other way (truth table → expression → gates), so
author it from an expression already in **sum-of-products** form (e.g.
`(a & ~b) | (~a & b)`): the given table, the answer expression, and the answer
circuit are then all the same single source.

### Hosting flowchart revision (Worksheet 9)

Just as the binary sheets (WS3/WS4) are bingen-hosted but mix in a few
boolgen/flowgen revision questions, a boolgen sheet can mix in a few **flowgen**
flowchart-tracing problems. Worksheet 9 is the example: it lists ordinary
`flowgen` `TRACE(...)` problems alongside the Boolean ones, and `boolgen.build`
reuses flowgen's own flowchart renderer and block typesetter for them (same
"reuse, not reimplement" approach as bingen — there is still no generic
multi-topic engine). `flowgen`'s `TRACE` also grew a `reveal=` argument: a note
shown *after* the trace table, used on WS9 to name the real-world algorithm a
flowchart implements only once the student has finished tracing it.

## Setup (one time)

```bash
make setup            # creates .venv and installs deps
brew install tectonic # if not already installed
git config core.hooksPath .githooks   # pre-commit hook: rebuilds + stages PDFs
```

The pre-commit hook (`.githooks/pre-commit`) rebuilds the affected worksheet
PDFs whenever generator sources or worksheet modules are staged, and stages the
regenerated PDFs so the checked-in PDFs never drift from the sources.

## Authoring

Edit `worksheet_1_boolean_algebra.py`:

```python
from gens.boolgen import parse, CIRCUIT, TRUTHTABLE

TITLE = "Worksheet 1: Boolean Algebra"

PROBLEMS = [
    parse("(a & b) | ~c"),                 # circuit -> expression + truth table
    CIRCUIT(parse("a & (b | c)")),         # expression -> draw the circuit
    TRUTHTABLE(parse("(a & b) | c")),      # expression -> draw the truth table
]
```

Expression syntax: `&`=AND, `|`=OR, `~`=NOT, `^`=XOR, and functions
`nand(...)`, `nor(...)`, `xnor(...)`. Parenthesise freely.

## Build

```bash
make boolean                                    # build worksheet_1_boolean_algebra.pdf
# same thing, explicitly (run from the repo root):
WS=worksheets/worksheet1_boolean_algebra
python -m gens.boolgen.build $WS/worksheet_1_boolean_algebra.py --out $WS/build
python -m gens.boolgen.build $WS/worksheet_1_boolean_algebra.py --out $WS/build --no-pdf  # figures + .tex only
```

The per-problem `figs/pNN.png` / `.svg` are the standalone diagram images for
use outside the worksheet.

## Roadmap

- **Flowcharts** for upcoming problem sets — same single-source pattern; add a
  `boolgen/flowchart.py` renderer and a new problem kind, reusing the worksheet
  /answer-key assembly in `latex.py`.
- Randomized variants (shuffle inputs / swap gates) from a seed.
- K-maps (schemdraw has a `Kmap` element; sympy can minimize).

## Layout

```
gens/boolgen/
  expr.py      expression model + parser + evaluate + truth_table  (source of truth)
  problem.py   problem kinds: DIAGRAM / CIRCUIT / TRUTHTABLE
  diagram.py   Expr -> schemdraw gate diagram (pdf/png/svg)
  simplify.py  sympy bridge: minimal / De Morgan form for the answer key
  latex.py     engineering-notation formula + truth table + document assembly
  build.py     CLI: worksheet module -> figures + combined PDF
worksheets/worksheet1_boolean_algebra/worksheet_1_boolean_algebra.py   the questions
```

---

## flowgen — flowcharts of simple algorithms

Each algorithm is authored once as a small statement tree (`read`, `assign`,
`out`, `If`, `While`); the flowchart, the pseudocode, and the trace table are all
derived from it. Flowcharts are drawn with **Graphviz** (auto-layout, including
loop back-edges).

Four problem types:

| In `worksheet_2_flowcharts.py`        | Student is given…        | …and must produce       |
|------------------------------------|--------------------------|-------------------------|
| `TRACE(algo, {"n": 4})`            | the flowchart + inputs   | the completed trace table |
| `DRAW(algo)`                       | the pseudocode           | the flowchart           |
| `OUTPUTS(algo, [{"n": 7}, ...])`   | the flowchart + a table of inputs | the output for each input |
| `DEBUG(algo, bug, cases=[...], description=…)` | a flowchart with ONE wrong box, what it should do, and should-print vs actually-prints | the box that is wrong, its correction, and why |

Authoring:

```python
from gens.flowgen import Algorithm, read, assign, out, While, TRACE, DRAW

sum_1_to_n = Algorithm("Sum 1..n", [
    read("n"), assign("sum", "0"), assign("i", "1"),
    While("i <= n", [assign("sum", "sum + i"), assign("i", "i + 1")]),
    out("sum"),
])

PROBLEMS = [TRACE(sum_1_to_n, {"n": 4}), DRAW(sum_1_to_n)]
```

Expressions/conditions are plain strings (`"sum + i"`, `"n % 2 == 0"`) — the same
string is both shown to the student and executed by the tracer.

```
gens/flowgen/
  algo.py       statement model + pseudocode + run() interpreter  (source of truth)
  flowchart.py  Algorithm -> Graphviz flowchart (pdf/png/svg)
  problem.py    problem kinds: TRACE / DRAW / OUTPUTS / DEBUG
  bug.py        DEBUG's mutators: plant one mistake in a correct algorithm
  latex.py      pseudocode + trace table + document assembly
  build.py      CLI: worksheet module -> figures + worksheet/answers PDFs
worksheets/worksheet2_flowcharts/worksheet_2_flowcharts.py   the questions
gens/wsbase.py      shared LaTeX setup (page geometry, cs17.org footer, Tectonic)
```

A worksheet module may also define `LEAD` — a paragraph of instructions shown
under the title on the worksheet (not on the answer key).

### DEBUG — find the one wrong box (Worksheet 20)

`DEBUG` inverts tracing: the student is given a flowchart that is *nearly* right
and has to work backwards from a wrong output to the box that caused it. The
**correct** algorithm stays the single source of truth; the mistake is a one-line
mutation applied to a copy of it (`gens/flowgen/bug.py`):

```python
DEBUG(pass_fail, wrong_cond("marks >= 40", "marks > 40"),
      cases=[{"marks": 72}, {"marks": 40}, {"marks": 12}],
      description="A student passes if they score 40 marks or more. …",
      why="40 marks must pass, so the test has to include 40 itself. …")
```

From that pair everything is derived, so the planted bug, the symptom, and the
correction can never disagree: the **buggy flowchart** (the mutated copy), the
**should print** column (running the correct algorithm), the **actually prints**
column (running the buggy one — a runaway loop is cut off and labelled *never
stops*), and the answer key's **fix** (each mutator reports the box it touched
and what it should say) plus the **corrected flowchart**. `why` is the only
authored prose. Available mutators, one per mistake beginners actually make:

| Mutator | The mistake |
|---------|-------------|
| `wrong_cond(old, new)` | a decision tests the wrong thing (`>=` vs `>`, `and` vs `or`, an off-by-one loop test) |
| `wrong_assign(var, old, new)` | a box computes/initialises the wrong value (`sum = 1` instead of `0`) |
| `wrong_print(old, new)` | the program prints the wrong variable (the total, not the average) |
| `swap_branches(cond)` | the Yes and No arms are the wrong way round |
| `missing(line)` | a box is left out — e.g. the counter update, so the loop never ends |
| `move_into_loop(line)` | a box that belongs after the loop was drawn inside it |

Every mutator asserts it matched exactly one statement, and applying a bug
asserts the pseudocode actually changed — a bug can never silently fail to apply
and leave a "buggy" chart that is in fact correct.

Needs the `dot` binary: `brew install graphviz`.

---

## bingen — number bases

Every problem is authored once and the answers are derived, so they can't drift:

- a **conversion** problem is just a list of integers written in some base — the
  target representation and the place-value / nibble working on the answer key
  are both computed from the same integer;
- a **decode** problem is one plaintext message — each character's ASCII code,
  in 8-bit binary, is derived from it, so the codes the student sees and the
  decoded answer can never disagree.

The full 0–127 ASCII chart (control mnemonics + printable characters) is itself
generated from the model and printed once as a reference whenever a worksheet
contains a decode problem.

Problem types:

| In a worksheet module               | Student is given…           | …and must produce        |
|-------------------------------------|-----------------------------|--------------------------|
| `TODECIMAL("1011", "1100", ...)`    | binary numbers              | each one in decimal      |
| `TOBINARY(6, 19, 42, ...)`          | decimal numbers             | each one in binary       |
| `CONVERT([...], frm="hex", to="bin")` | numbers in one base       | each one in another base (bin/dec/hex) |
| `DECODE("HI")`                      | ASCII codes in binary + the ASCII table | the decoded message |
| `BITMAP([...])`                     | a picture's rows as hex bytes | convert + shade the 1-bits → the image appears |
| `IPV4(["192.168.1.1", ...])`        | IPv4 addresses              | each byte in 8-bit binary (+ spot the &gt;255 one) |

`CONVERT` handles any direction among `bin` / `dec` / `hex`; the answer key shows
place-value working for `→ dec`, base-16 place values for `dec → hex`, and 4-bit
nibble grouping for `bin ↔ hex`.

`BITMAP` is the real-world tie-together: a black-and-white image is a grid of
pixels, one byte per row. The picture is authored once as ASCII art (`'#'` /
`'.'`); the hex bytes the student converts are derived from it, and the answer
key fills the grid (via `\cellcolor`) to reveal the image — so the bytes and the
picture can never disagree.

### Mixing in revision questions

`worksheet_3_binary.py` (**Worksheet 3**) and `worksheet_4_hexadecimal.py` (**Worksheet 4**)
are number-base sheets that also sprinkle in a couple of Boolean-algebra
questions and a flowchart trace as revision of Worksheets 1 and 2. There's no
generic multi-topic engine: the worksheet simply lists ordinary `boolgen` /
`flowgen` problem objects alongside the conversion ones, and `bingen.build`
reuses those generators' own renderers (and figure output) to typeset them. So a
sheet that contains a Boolean or flowchart problem *does* get a `figs/`
directory; a pure-conversion sheet does not.

```python
from gens.bingen import TODECIMAL, DECODE
from gens.boolgen import parse, DIAGRAM, TRUTHTABLE
from gens.flowgen import Algorithm, read, assign, out, If, While, TRACE

TITLE = "Worksheet 3: Binary"

PROBLEMS = [
    TODECIMAL("1011", "1100", "0111"),   # binary -> decimal
    DIAGRAM(parse("(a & b) | ~c")),      # revision: read the gate diagram
    DECODE("CS17"),                      # ASCII codes -> message
    TRUTHTABLE(parse("a ^ (b & c)")),    # revision: draw the truth table
    TRACE(digit_stats, {"n": 6391}),     # revision: trace the flowchart
]
```

```
gens/bingen/
  binary.py    binary <-> decimal + ASCII table model  (source of truth)
  convert.py   bin/dec/hex parse, format + place-value / nibble working
  pixel.py     ASCII-art bitmap -> per-row bits / hex byte  (source of truth)
  problem.py   problem kinds: TODECIMAL / TOBINARY / CONVERT / DECODE / BITMAP / IPV4
  latex.py     ASCII reference + conversion lines + decode/pixel grids + assembly;
               dispatches Boolean/flowchart problems to boolgen/flowgen
  build.py     CLI: worksheet module -> worksheet/answers PDFs (+ figs as needed)
worksheets/worksheet3_binary/worksheet_3_binary.py   the questions (Worksheet 3)
worksheets/worksheet4_hexadecimal/worksheet_4_hexadecimal.py the questions (Worksheet 4)
```

---

## scratchgen — Scratch build-along sheets (A–G)

Worksheets 12–19 are **follow-along** sheets: not trace-and-predict, but small
projects the student builds in Scratch at the computer. Unlike the other
generators (which model an *algorithm* and derive a picture), scratchgen models a
**Scratch script directly** — a hat block plus the stack beneath it, exactly as it
appears on the code canvas. Each finished script is authored once, in Python, and
rendered as real Scratch blocks with the **`scratch3`** LaTeX package, so the
picture the student matches can never drift from the prose build steps that
describe it.

The unit is a `BUILD(...)` **project**: a goal, the new blocks it introduces,
ordered build steps, the finished script(s) to match, and a required "Your task"
section of progressive enhancements. A `gap(...)` leaves a grey "your turn" hole
in a script — a plain-words hint on the worksheet, the real block on the answer
key — which is how the E/F/G capstones ask the student to supply the key pieces.

The sheets ramp A → G:

| Sheet | WS | Game / focus | New power |
|---|---|---|---|
| Scratch A | 12 | first projects | basic blocks, movement, events |
| Scratch B | 13 | sensing & choices | `touching?`, `if`, key sensing |
| Scratch C | 14 | variables & score | `set` / `change` a variable |
| Scratch D | 15 | Maze Quest (multi-sprite game) | `broadcast` / `when I receive` |
| Scratch E | 17 | Coin Dash (gap-fill capstone) | assembling a whole game |
| Scratch F | 18 | Rock Dodge (gap-fill capstone) | falling + off-screen tests |
| Scratch G | 19 | **Space Invaders** (reference build) | **clone coordination** + custom blocks |

**Scratch G** is the big capstone — a full Space Invaders shown as a finished
reference build. Its headline idea is *many clones sharing one brain*: one Invader
sprite stamps out 55 clones that march, drop, and reverse as a single organism,
steered by shared variables and a broadcast "conductor". It also introduces
custom blocks (`define` / call), clone blocks (`create clone of` / `delete this
clone` / `when I start as a clone`), and reproduces the arcade's famous
speed-up. The costumes come from `scratch-invaders/` (run its `slice_sprite.py`).

Authoring (a `BUILD` project, rendered via `script(...)`):

```python
from gens.scratchgen import (
    BUILD, script, when_flag, forever, if_, key_pressed, changex, gap,
)

p1 = BUILD(
    "The ship",
    goal="Drive the player ship left and right along the bottom row.",
    steps=["Add a forever loop that reads the arrow keys."],
    scripts=script(
        when_flag(),
        forever(
            if_(key_pressed("left arrow"), changex(-6)),
            if_(key_pressed("right arrow"), changex(6)),
        ),
        caption="Player: drive left/right",
    ),
    tasks=[("Tune the speed to taste.", "The ship feels right.")],
)

TITLE = "Scratch G"
ACTIVITIES = [p1]           # build.py reads TITLE + ACTIVITIES (+ optional PALETTE, LEAD)
```

Build (all Scratch sheets share the generator, so they rebuild together):

```bash
make scratch    # gens.scratchgen -> worksheets/worksheet12..19/build/
# one sheet, explicitly:
WS=worksheets/worksheet19_scratch_invaders
python -m gens.scratchgen.build $WS/worksheet_19_scratch_invaders.py --out $WS/build
```

```
gens/scratchgen/
  script.py    the Scratch-script model: hat + blocks (events, motion, looks, sound,
               control, sensing, operators, variables, clones, My Blocks)  (source of truth)
  problem.py   the BUILD activity (goal / new blocks / steps / scripts / tasks)
  render.py    Script -> scratch3 LaTeX (category picks the colour, C-blocks recurse)
  latex.py     front matter + colour key + activity layout + document assembly
  build.py     CLI: worksheet module -> worksheet/answers PDFs
worksheets/worksheet19_scratch_invaders/worksheet_19_scratch_invaders.py   Scratch G (Space Invaders)
```

Needs the `scratch3` LaTeX package (Tectonic auto-downloads it) and the
**Geist Mono** font installed for the CS17 wordmark in the shared heading.

---

## papergen — graded question papers

Everything above generates **worksheets**: a flat list of practice problems, no
weighting. A **paper** is a different object, so it gets its own generator:

- **sections** (Section A, Section B), each with its own scenario and questions;
- a **marks budget** — a part carries marks, a question totals its parts, a
  section totals its questions, and `Paper.check()` raises if the declared
  `max_marks` disagrees with what the parts actually add up to, so a paper can
  never go to print claiming a total it doesn't have;
- **exam chrome** — duration, maximum marks, and a general-instructions box.

The worksheets' single-source habit is kept wherever there is something to
derive. A Calc question's data is authored **once** as a `Workbook` (`sheet.py`)
and every figure on the answer key is *computed* from it — the totals, the
SUMIFS answers, the region summary, the pivot with both margins, and which
region comes top. Edit a unit price and the tables the student is given and the
key's numbers move together. Spreadsheet row numbers are derived too, so the
cell references in the question text (`in cell I18`) follow the data.

```python
WB = Workbook(PRODUCTS, SALES)          # the single source
...
answer_items=(fx(f"I{TOTAL_ROW}  =SUM(I{FIRST}:I{LAST})") +
              r"$\rightarrow$ \textbf{%s}" % rupees(WB.grand_total()),)
```

Scratch answers reuse **scratchgen**: the model solution is authored as ordinary
`script(...)` objects and drawn by `scratchgen.render_script`, so a paper's
blocks and the build-along sheets' blocks are the same picture (same
"reuse, not reimplement" approach as bingen dispatching to boolgen/flowgen).
`gens/scratchgen/latex.py` exposes its scratch3 setup as `SCRATCH_EXTRA` for
this; papergen appends its own exam macros to it.

**Paper 1** is the practical: Section A a GreenLeaf Organics data-handling task
in Calc (XLOOKUP, SUMIFS/SUMIF, a chart and a pivot table, 10 marks), Section B
the Apple Catcher Scratch game (15 marks). 25 marks, 1 hour 45 minutes.

**Paper 2** is a 10-minute hand-out rather than an exam (4 marks): one small
Scratch script — a `repeat` loop around an `if/else`, over two variables — that
the student traces on paper to predict its output. It is the other direction
from the build-along sheets: the script is *given* (`Question.given`, shown on
both documents) and the answer is what it prints. Its loop constants drive both
the blocks and a Python run of the same loop, so the trace table and the final
answer on the key are computed rather than typed. Being a single question it
uses an unnamed `Section`, which drops the section band.

```bash
make papers     # both papers
make paper1     # gens.papergen -> papers/paper1_practical/build/
make paper2     # gens.papergen -> papers/paper2_trace/build/
# paper only, no answer key (what you print for the exam):
python -m gens.papergen.build papers/paper1_practical/paper_1_practical.py \
       --out papers/paper1_practical/build --paper-only
```

```
gens/papergen/
  sheet.py     the workbook: products + sales, and every figure derived from them
  paper.py     Paper / Section / Question / Part / SheetTable + the marks check
  latex.py     exam chrome, spreadsheet grids, per-part marks, document assembly;
               reuses scratchgen for Scratch solutions
  build.py     CLI: paper module -> paper + answer-key PDFs
papers/paper1_practical/paper_1_practical.py   the practical (Calc + Scratch)
papers/paper2_trace/paper_2_trace.py           the trace hand-out
```

---

## termgen — terminal & shell drills

Worksheet 21 is the only sheet that is done at a real terminal, so it is the only
one that ships a **hand-out beside its PDFs**: `cs17-archive.zip`, a deliberately
messy folder the student extracts and then tidies up with commands. It is also
the only one built in **two formats** — the printed PDF and a **Markdown page for
the wiki** — from the same source, so the hand-out and the published assignment
cannot drift apart.

## How it works

The archive is authored **once**, as a tree of `D` (folder) / `F` (text file) /
`IMG` (real JPEG or PNG) nodes — the single source of truth. From that one tree
the generator derives, so they can never disagree:

- the **zip** the student extracts (`tree.make_zip`, fixed timestamps so rebuilds
  do not churn it)
- the **ASCII map**, which is written into the archive's own `README.txt` and
  printed on the answer key — not on the worksheet, see below
- every **number in the answer key** — `wc -l` totals, how many lines `grep`
  matches, how many files a `*` picks up — read back out of the same content with
  `nlines`, `ngrep`, `match`, `listing`

The names in the archive are chosen to make the shell's rough edges show up:
long names (Tab completion), a folder with spaces (quoting and escaping) and a
three-deep folder (`../../..`). What the archive does **not** contain is just as
deliberate: there is no `gallery/`, no `backup/` and no `sorted/`. Every folder
the student moves things into is one they make themselves with `mkdir`.

## The shape of the sheet: one tidy-up, in order

The parts are the steps somebody actually takes when clearing out a messy
folder, and each command is met at the moment that step needs it — rather than
walking the command list and inventing a use for each entry.

| Part | Step | Commands it needs |
|---|---|---|
| 1 | look at the mess | `pwd` `ls` `ls -l` `ls -a` `cd` `..` `~` `cat` |
| 2 | build the shelves | `mkdir`, `mkdir -p`, and its two errors |
| 3 | move everything in | Tab, quoting, `*`, `mv`, `cp` |
| 4 | throw out what is left | `rm` `rmdir` `--help` `man`, case, safety |
| 5 | find things and count | `history` `grep` `wc` |
| 6 | join commands up | `|` `>` `>>` `touch` `echo` `cowsay` |
| 7 | save your history | `history > history.txt`, `submission/`, `zip -r` |

Folders before files is the load-bearing decision. Because the zip ships with
nowhere tidy to put anything, Part 3 fills shelves the student built in Part 2,
and Part 4 can reason about what is left over instead of being told.

Two rules keep that honest. **Every folder Part 2 makes is one a later part
fills** — `mkdir -p` is taught on `sorted/notes`, which Part 3 moves the club's
notes into, not on a throwaway. And **Part 4 only ever deletes things that came
in the zip**: `inbox/old-phone-photos` (shipped empty), `documents/temp` (a junk
file and a stray `New Folder`) and `documents/drafts`. Asking a student to
create a folder and then delete it teaches the command but not the judgement,
which is the whole point of putting deletion last.

**The parts are strictly cumulative.** Part 3 moves into folders Part 2 made,
Part 4 deletes folders Part 3 emptied, Part 6 counts what Part 3 put there, and
Part 7 hands in files Part 6 wrote. A task inserted into one part can invalidate
the state a later part assumes, so after editing, run the whole sequence against
the freshly built zip before trusting the key.

**The map is not printed on the worksheet.** It lives in the archive's own
`README.txt`; Part 1 has the student print it with `cat` and copy it out by hand
into a `BOX`, which is the sheet's first use of the terminal as a source of
truth. The answer key prints the map, for marking.

> **No two names may differ only in case.** macOS (APFS) and Windows are case
> *insensitive* by default, so `Notes.txt` and `notes.txt` in the same folder do
> not both survive the unzip — one silently overwrites the other and the printed
> map stops matching what the student sees. `tree.check_case_collisions` refuses
> such a tree at build time. Case sensitivity is taught through command names,
> options and `grep` instead, which are case sensitive on every machine.

> **The sheet targets one platform: Ubuntu Desktop, so bash and GNU coreutils.**
> Every error message quoted in the answer key is the exact wording the student
> will see, verified by running the whole sheet against `ubuntu:24.04` in Docker.
> It is not interchangeable with macOS: `cp` says `cannot stat 'missing.txt'`
> where BSD says `missing.txt`, `rmdir` says `failed to remove 'logs'`, an
> unmatched `*` reaches `ls` instead of being rejected by the shell, and `LS`
> and `cat NOTES.txt` fail on Ubuntu but succeed on a Mac. Re-verify against a
> container before retargeting the sheet. `unzip` and `zip` are safe to use in
> tasks: `ubuntu-desktop` pulls in both. `cowsay` is **not** installed, so the
> sheet prints `sudo apt install cowsay` as a `given` command; it lands in
> `/usr/games`, which is on Ubuntu's default PATH but not inside the
> `ubuntu:24.04` image, so a container check of it needs the PATH set by hand.

## Authoring

A sheet is a list of `PART`s, each a list of plain-English `TASK`s — the action on
the worksheet, the model command and its expected output on the **answer key
only** (the lesson plan's teacher note: do not hand out a one-to-one command
list). The one exception is `given=`, which prints its commands on the worksheet
too — for a command the sheet neither teaches nor tests, such as the `unzip` that
has to happen before lesson 1 exists. Three drills are write-in tables instead of
list items, because writing the answer by hand *is* the exercise: `PATHS`
(relative vs absolute), `ERRORS` (run it, copy the message back, say why) and
`PREDICT` (write your prediction, then press Enter). A fourth unit is not a
drill but a blank: `BOX` reserves a framed, ruled-free area — empty on the
worksheet, filled with `answer=` on the key — for something whose *shape*
matters and that a run of ruled lines would flatten, such as an indented tree.

```python
PART("Where am I?", lesson="Lesson 1", recap=[("pwd", "print the folder you are in")],
     tasks=[TASK(r"Print where you are.", cmd="pwd", expect="/Users/...", write=1),
            PATHS([("cs17-archive", "logs", "logs", "~/.../cs17-archive/logs")])])
```

Build:

```bash
make terminal
# explicitly, and without rebuilding the zip:
WS=worksheets/worksheet21_terminal_shell
python -m gens.termgen.build $WS/worksheet_21_terminal_shell.py --out $WS/build --no-zip
```

`make pdfs` collects the two PDFs like any other sheet; the **zip is not copied**
into `pdfs/` — hand it out from `worksheets/worksheet21_terminal_shell/build/`.

```
gens/termgen/
  tree.py     the archive: D/F/IMG nodes, queries (nlines/ngrep/match/listing),
              ascii_tree, materialise + make_zip, check_case_collisions  (source of truth)
  task.py     TASK / PATHS / ERRORS / PREDICT and the PART that holds them
  latex.py    the printed sheet: ruled answer lines, write-in tables, verbatim text
  markdown.py the same sheet as a wiki page (LaTeX prose -> Markdown, see below)
  build.py    CLI: worksheet module -> PDFs + Markdown + the zip
worksheets/worksheet21_terminal_shell/worksheet_21_terminal_shell.py   Worksheet 21
```

## The three outputs

`build.py` writes, from the one worksheet module: `<name>.pdf` / `<name>.md`
(the student's sheet, printed and as a wiki page), `<name>-answers.pdf` /
`<name>-answers.md` (the teacher's), `terminal-shell-cheat-sheet.pdf` (the
one-page card) and `cs17-archive.zip` (the hand-out). `make pdfs` collects every
PDF, the cheat sheet included; copy the Markdown out of the worksheet's `build/`
folder.

**The cheat sheet** (`cheatsheet.py`) is the only thing here that does not go
through LaTeX. It is a dense two-column card, which CSS columns do in a few
lines, so it is HTML printed by **headless Chrome** (`--print-to-pdf`). Chrome
is optional: a missing one warns and skips the card rather than failing the
build. The budget is **two pages** — two sides of one sheet of paper.

It is styled with **frappe-ui's design tokens and type scale**. There is no
Tailwind preset to pull from on a printed page, so the light-mode values are
resolved from frappe-ui's own `tailwind/generated/{colors,typography,radius}.json`
(1.0.0-beta.21) and declared as custom properties under their token names
(`--ink-gray-9`, `--surface-gray-1`, `--outline-gray-2`, `--radius-4`, …).
Three of the design language's rules drive the look:

- **Sentence case headings.** Frappe UIs never shout a heading, so a section is
  marked by weight and colour (`ink-gray-5`, `text-sm`, 600), never by capitals.
- **The tight/loose split.** A one-line label takes the tight scale (`text-xs`,
  line-height 1.15); anything that wraps takes the loose one (`text-p-2xs`, 1.6).
- **"Gray everywhere, except where colour encodes meaning."** Headings, commands
  and output are all gray. Amber appears only on the caution boxes, red only on
  the one irreversible warning (`rm`).

Two departures, both because a printed reference is not an app screen: frappe-ui
ships no monospace token (its scale is Inter only), so command text uses Geist
Mono at the 11px `text-2xs` step; and the whole card is rendered at `zoom: 0.84`
so the screen-tuned scale fits two sides of A4 — the same type system at 84%,
rather than a pile of one-off sizes that match no step on the scale.

It deliberately does **not** use the assignment archive. A reference should
still make sense a year later, long after `cs17-archive` has been deleted, so
every example runs in one tiny made-up folder, `~/work`, printed at the top of
the card. Each entry carries a real transcript and, where the output needs it, a
pointer block built by `FIELDS`, which takes the columns from the output line
itself so the arrows cannot drift away from what they point at:

```
$ wc notes.txt
  3  37 194 notes.txt
  |  |  |
  |  |  `- characters
  |  `---- words
  `------- lines
```

Every output is copied from a real Ubuntu run of `~/work` — including the ones
that differ between a terminal and a pipe (`ls` prints columns on a tty, one
name per line into a pipe). Rebuild that folder in a container and re-verify
after editing an example. CSS columns **drop** whatever does not fit instead of
reporting it, so `build.py` counts the pages and warns past two; never silence
that warning by capping the column height. `cheatsheet.overlong` likewise warns
about any transcript line past `MAX_COLS` (52 characters at the mono step and
column width), which `overflow: hidden` would otherwise clip without a word. A heading, its intro and its first
entry ship inside one unbreakable `.lead` box, because the `break-before` hints
alone are advisory in multicol and leave headings stranded at a column foot.

Only two things differ between the formats, and both are authored deliberately:

- **Where answers go.** Ruled lines are a paper device, so the module holds
  `ANSWER_NOTE` (print: "write on this sheet") and `ANSWER_NOTE_MD` (web: "keep
  your answers in your own document"), and each renderer takes its own.
- **How prose is translated.** Part intros, notes and captions are authored once
  as LaTeX, carrying `\cmd{...}`, `\emph{...}`, boxes and lists on purpose.
  `markdown._md` converts exactly the macros this generator uses and **raises on
  any macro it does not know**, so a new one fails the build instead of leaking
  `\cmd{` onto the wiki. Code spans are stashed behind placeholders and restored
  last — otherwise `~` in `\cmd{~/Desktop}` would be eaten as a LaTeX hard space.

Everything else — task text, commands, expected output, every table — comes from
the same `PARTS` list, so the printed sheet and the wiki page always agree.

Needs **Pillow** (the archive's `.jpg`/`.png` files are generated, not committed)
and the `fancyvrb` / `longtable` LaTeX packages, which Tectonic auto-downloads.
The cheat sheet additionally needs **Google Chrome or Chromium** on the PATH (or
in `/Applications`); without it the other outputs still build.
