# cs17 — practice-worksheet generators

Generators for **cs17.org** practice worksheets. Each produces two polished PDFs
— the worksheet and a separate answer key — plus standalone diagram images
(PNG/SVG) for reuse elsewhere (slides, web, etc.).

- **`boolgen`** — Boolean algebra (logic-gate diagram ↔ expression ↔ truth table).
- **`flowgen`** — flowcharts of simple algorithms (flowchart ↔ pseudocode ↔ trace table).

Both share the same idea: author each problem **once** as a single source of
truth, then derive every representation from it so they can't disagree. Build:

```bash
make            # both worksheets
make boolean    # boolgen  -> build/worksheet/
make flowchart  # flowgen  -> build/flowchart_worksheet/
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
worksheet.py ──▶ boolgen ──▶ build/worksheet/
                              ├── figs/pNN.{pdf,png,svg}  ← reusable diagram images
                              ├── worksheet.pdf           ← questions
                              └── worksheet-answers.pdf   ← answer key (separate)
```

## Three problem types

All authored from the same expression; the *type* picks which direction the
student works:

| In `worksheet.py`          | Student is given… | …and must produce            |
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

Edit `worksheet.py`:

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
make                                    # build worksheet.pdf
python -m boolgen.build worksheet.py    # same thing
python -m boolgen.build worksheet.py --no-pdf   # figures + .tex only
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
worksheet.py   the questions
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
