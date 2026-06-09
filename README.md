# cs17 — practice-worksheet generators

Generators for **cs17.org** practice worksheets. Each produces two polished PDFs
— the worksheet and a separate answer key — plus standalone diagram images
(PNG/SVG) for reuse elsewhere (slides, web, etc.).

- **`boolgen`** — Boolean algebra (logic-gate diagram ↔ expression ↔ truth table).
- **`flowgen`** — flowcharts of simple algorithms (flowchart ↔ pseudocode ↔ trace table).
- **`bingen`** — number bases (binary ↔ decimal ↔ hexadecimal, ASCII codes → message).

All share the same idea: author each problem **once** as a single source of
truth, then derive every representation from it so they can't disagree. Build:

```bash
make            # all worksheets
make boolean    # boolgen  -> build/boolean_worksheet/
make flowchart  # flowgen  -> build/flowchart_worksheet/
make binary     # bingen   -> build/binary_worksheet/   (Worksheet 3)
make hex        # bingen   -> build/hex_worksheet/       (Worksheet 4)
```

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
boolean_worksheet.py ──▶ boolgen ──▶ build/boolean_worksheet/
                              ├── figs/pNN.{pdf,png,svg}  ← reusable diagram images
                              ├── boolean_worksheet.pdf         ← questions
                              └── boolean_worksheet-answers.pdf ← answer key (separate)
```

## Three problem types

All authored from the same expression; the *type* picks which direction the
student works:

| In `boolean_worksheet.py`  | Student is given… | …and must produce            |
|----------------------------|-------------------|------------------------------|
| `parse("...")`             | the gate diagram  | the expression + truth table |
| `CIRCUIT(parse("..."))`    | the expression    | the logic-gate circuit       |
| `TRUTHTABLE(parse("..."))` | the expression    | the truth table (≤ 3 vars)   |

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

Edit `boolean_worksheet.py`:

```python
from boolgen import parse, CIRCUIT, TRUTHTABLE

TITLE = "Boolean Algebra Worksheet"

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
make boolean                                    # build boolean_worksheet.pdf
python -m boolgen.build boolean_worksheet.py    # same thing
python -m boolgen.build boolean_worksheet.py --no-pdf   # figures + .tex only
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
boolgen/
  expr.py      expression model + parser + evaluate + truth_table  (source of truth)
  problem.py   problem kinds: DIAGRAM / CIRCUIT / TRUTHTABLE
  diagram.py   Expr -> schemdraw gate diagram (pdf/png/svg)
  simplify.py  sympy bridge: minimal / De Morgan form for the answer key
  latex.py     engineering-notation formula + truth table + document assembly
  build.py     CLI: worksheet module -> figures + combined PDF
boolean_worksheet.py   the questions
```

---

## flowgen — flowcharts of simple algorithms

Each algorithm is authored once as a small statement tree (`read`, `assign`,
`out`, `If`, `While`); the flowchart, the pseudocode, and the trace table are all
derived from it. Flowcharts are drawn with **Graphviz** (auto-layout, including
loop back-edges).

Three problem types:

| In `flowchart_worksheet.py`        | Student is given…        | …and must produce       |
|------------------------------------|--------------------------|-------------------------|
| `TRACE(algo, {"n": 4})`            | the flowchart + inputs   | the completed trace table |
| `DRAW(algo)`                       | the pseudocode           | the flowchart           |
| `OUTPUTS(algo, [{"n": 7}, ...])`   | the flowchart + a table of inputs | the output for each input |

Authoring:

```python
from flowgen import Algorithm, read, assign, out, While, TRACE, DRAW

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
flowgen/
  algo.py       statement model + pseudocode + run() interpreter  (source of truth)
  flowchart.py  Algorithm -> Graphviz flowchart (pdf/png/svg)
  problem.py    problem kinds: TRACE / DRAW
  latex.py      pseudocode + trace table + document assembly
  build.py      CLI: worksheet module -> figures + worksheet/answers PDFs
flowchart_worksheet.py   the questions
wsbase.py      shared LaTeX setup (page geometry, cs17.org footer, Tectonic)
```

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

`binary_worksheet.py` (**Worksheet 3**) and `hex_worksheet.py` (**Worksheet 4**)
are number-base sheets that also sprinkle in a couple of Boolean-algebra
questions and a flowchart trace as revision of Worksheets 1 and 2. There's no
generic multi-topic engine: the worksheet simply lists ordinary `boolgen` /
`flowgen` problem objects alongside the conversion ones, and `bingen.build`
reuses those generators' own renderers (and figure output) to typeset them. So a
sheet that contains a Boolean or flowchart problem *does* get a `figs/`
directory; a pure-conversion sheet does not.

```python
from bingen import TODECIMAL, DECODE
from boolgen import parse, DIAGRAM, TRUTHTABLE
from flowgen import Algorithm, read, assign, out, If, While, TRACE

TITLE = "Worksheet 3"

PROBLEMS = [
    TODECIMAL("1011", "1100", "0111"),   # binary -> decimal
    DIAGRAM(parse("(a & b) | ~c")),      # revision: read the gate diagram
    DECODE("CS17"),                      # ASCII codes -> message
    TRUTHTABLE(parse("a ^ (b & c)")),    # revision: draw the truth table
    TRACE(digit_stats, {"n": 6391}),     # revision: trace the flowchart
]
```

```
bingen/
  binary.py    binary <-> decimal + ASCII table model  (source of truth)
  convert.py   bin/dec/hex parse, format + place-value / nibble working
  pixel.py     ASCII-art bitmap -> per-row bits / hex byte  (source of truth)
  problem.py   problem kinds: TODECIMAL / TOBINARY / CONVERT / DECODE / BITMAP / IPV4
  latex.py     ASCII reference + conversion lines + decode/pixel grids + assembly;
               dispatches Boolean/flowchart problems to boolgen/flowgen
  build.py     CLI: worksheet module -> worksheet/answers PDFs (+ figs as needed)
binary_worksheet.py   the questions (Worksheet 3)
hex_worksheet.py      the questions (Worksheet 4)
```
