# Q1-P3 — Jugaad Hardware Sales Analysis: Walkthrough & Solutions

Reference solution for [`/student-handbook/assignments/q1-p3`](https://portal.cs17.org/student-handbook/assignments/q1-p3).

> **This folder (prep, not the published assignment).** The student-facing
> assignment is hand-written markdown on the wiki (link above). What lives here:
> - `build_seed.py` — regenerates `references/sales.xlsx` from scratch (`python build_seed.py`).
> - `references/sales.xlsx` — the seed workbook students start from.
> - `build_answer_key.py` — regenerates the worked solution (`python build_answer_key.py`).
> - `references/jugaad_sales_answers.xlsx` — the worked solution: title rows in
>   place and **every formula filled in** (Sales_Analysis, the two Sales helper
>   columns, all three Charts summary tables). Only the **four chart objects** are
>   left to insert by hand — that's the part the assignment grades. Open in
>   Calc/Excel and accept "recalculate" to see the numbers.
> - this file — the instructor walkthrough / answer key.

> **Continuation of [Q1-P2](../q1-p2_jugaad_inventory/).** Same business (Jaggu
> Uncle's *Jugaad Hardware & Tools*), so students reuse a catalogue they already
> know. Q1-P2 was about **stock**; **Q1-P3 is purely about sales** — turning the
> sales log into insight with modern lookups (`XLOOKUP`) and **charts**. There is
> no stock here: no opening stock, reorder levels, damages or returns — just the
> product catalogue and what was sold.

> **New since Q1-P2:** `XLOOKUP` (the modern replacement for `VLOOKUP`), the
> `LARGE` function, and the full charting workflow. `SUMIFS` and the
> no-hardcoding rule carry over from Q1-P2 and are only recapped.

> All formulas use LibreOffice's sheet-reference style (`.`). On Excel, swap `.`
> for `!`. **`XLOOKUP` needs Calc 7.5+ or Excel 365/2021** — confirm the lab
> machines, or use the `INDEX/MATCH` fallback (§3) as the primary path.

> After step 1 the three data sheets gain **two title rows on top**, so headers
> move to **row 3** and data starts at **row 4**. The `Charts` sheet ships
> pre-laid-out (title bar + empty summary tables) — students don't insert rows
> there. Every cell reference below accounts for this.

---

## 0. What students start from

`references/sales.xlsx` ships two populated sheets and two empty ones:

| Sheet | State on hand-out |
|---|---|
| `Item_Master` | populated product catalogue — A=Item ID, B=Item Name, C=Category, D=Brand, E=Unit, F=Cost Price, **G=Selling Price** (350 items) |
| `Sales` | populated sales log — A=Sale ID, B=Date, C=Item ID, D=Quantity, E=Invoice No (1 887 sales, Oct 2025 – Mar 2026) |
| `Sales_Analysis` | `Item ID` column pre-filled (`A4:A353`); headers present — students build §2–§3 |
| `Charts` | pre-laid-out skeleton — title bar + three empty summary tables (section titles + headers), students fill §4 |

> Every row in `Sales` is one sale (the old stock movements — purchases, damages,
> returns — are gone). So "how many did we sell" is a plain sum over `Sales`, no
> transaction-type filter needed.

---

## 1. Basics — sheet titles

Same as Q1-P2 §1 (insert 2 rows, merge `C1:D2`, black fill / white 16pt /
centered). Do it on the **three data sheets** so their data lines up at row 4:

- `Item_Master` → `Items: Jugaad Hardware & Tools`
- `Sales` → `Sales: Jugaad Hardware & Tools`
- `Sales_Analysis` → `Sales Analysis: Jugaad Hardware & Tools`

> `Charts` already has its title bar and an empty table skeleton — don't insert
> rows there; just fill it in (§4).

---

## 2. Sales_Analysis — per-item revenue

`Sales_Analysis` lists every `Item ID` down `A4:A353`. Write each formula in
**row 4** and fill down to **row 353**.

| Target column | Cell | Formula | Skill |
|---|---|---|---|
| Item Name | `B4` | `=XLOOKUP(A4, Item_Master.A:A, Item_Master.B:B)` | XLOOKUP (§3) |
| Category | `C4` | `=XLOOKUP(A4, Item_Master.A:A, Item_Master.C:C)` | XLOOKUP (§3) |
| Units Sold | `D4` | `=SUMIFS(Sales.D:D, Sales.C:C, A4)` | SUMIFS recap |
| Selling Price | `E4` | `=XLOOKUP(A4, Item_Master.A:A, Item_Master.G:G)` | XLOOKUP (§3) |
| Revenue | `F4` | `=D4*E4` | arithmetic |

> **Units Sold** sums the `Quantity` of every sale for that item — one criterion
> (the Item ID), since every `Sales` row is already a sale. `=SUMIF(Sales.C:C,
> A4, Sales.D:D)` would work too; we use `SUMIFS` to stay consistent with Q1-P2.

---

## 3. XLOOKUP — the modern lookup (NEW)

In Q1-P2 every cross-sheet pull was `VLOOKUP(key, range, col_number, 0)`.
`XLOOKUP` does the same job but you name the **lookup column** and the **return
column** directly — no counting columns, and it doesn't break when columns move.

```
=XLOOKUP(A4, Item_Master.A:A, Item_Master.G:G)
         │     │                │
         │     │                └─ return_array: what to bring back (Selling Price)
         │     └─ lookup_array:  where to find the key (Item ID column)
         └─ lookup_value:        the Item ID in this row
```

### VLOOKUP vs XLOOKUP — same result, why XLOOKUP wins

| | `VLOOKUP` (Q1-P2) | `XLOOKUP` (now) |
|---|---|---|
| Selling Price | `=VLOOKUP(A4, Item_Master.A:G, 7, 0)` | `=XLOOKUP(A4, Item_Master.A:A, Item_Master.G:G)` |
| Return column | a **number** (7) counted by hand | an **actual column** (`G:G`) |
| Insert a column in `Item_Master` | breaks (7 now points elsewhere) | still correct |
| Lookup column position | must be **left** of the data | can be anywhere |
| Default match | **fuzzy** — needs `0`/`FALSE` or it's wrong | **exact** by default (safer) |

> The `0` footgun from Q1-P2 disappears: `XLOOKUP` is exact-match by default.

### Not-found handling (NEW)

`XLOOKUP` has a built-in 4th argument for "no match" — no `IFERROR(...)` wrapper:

```
=XLOOKUP(A4, Item_Master.A:A, Item_Master.G:G, "Not found")
```

### Fallback if XLOOKUP is unavailable (older Calc/Excel)

`INDEX`/`MATCH` does the same thing and works everywhere:

```
=INDEX(Item_Master.G:G, MATCH(A4, Item_Master.A:A, 0))
```

---

## 4. Charts (NEW — the core of this assignment)

Charts plot a small **summary table**, not 350 raw rows. The `Charts` sheet
already has the three tables' **section titles + headers** laid out (row 4 =
titles, row 5 = headers, data from row 6) — students fill the cells **all by
formula** (the Q1-P2 no-hardcoding rule still applies), then **Insert → Chart…**,
pick the type, **Finish**, double-click to edit titles/labels.

### 4a. Summary table — Revenue by Category (feeds charts 1 & 3)

Under the pre-set `Category` / `Revenue` headers (`A5` / `B5`):

| Cell | Content |
|---|---|
| `A6:A15` | the 10 category names (Power Tools, Hand Tools, Hardware, Fasteners, Electrical, Plumbing, Paints & Coatings, Adhesives & Sealants, Safety Gear, Garden Tools) |
| `B6` | `=SUMIFS(Sales_Analysis.F:F, Sales_Analysis.C:C, A6)` → fill to `B15` |

### 4b. Summary table — Monthly Revenue (feeds chart 2)

Monthly revenue needs the **sale-by-sale** data (the per-item sheet has no date
column), so add **two helper columns** to `Sales` — more XLOOKUP practice in a
real second context:

| Sales | Cell | Formula |
|---|---|---|
| `Sale Value` (new col F) | `F4` | `=D4*XLOOKUP(C4, Item_Master.A:A, Item_Master.G:G)` |
| `Month` (new col G) | `G4` | `=TEXT(B4, "MMM YYYY")` |

Fill both down to row **1890** (the last sale). Then on `Charts`, under the
pre-set `Month` / `Revenue` headers (`D5` / `E5`), the six months in order:

| Cell | Content |
|---|---|
| `D6:D11` | `Oct 2025`, `Nov 2025`, `Dec 2025`, `Jan 2026`, `Feb 2026`, `Mar 2026` |
| `E6` | `=SUMIFS(Sales.F:F, Sales.G:G, D6)` → fill to `E11` |

> Simpler alternative if you want to drop the price lookup: chart **units sold
> per month** instead of revenue — then you only need the `Month` helper and
> `=SUMIFS(Sales.D:D, Sales.G:G, D6)`.

### 4c. Summary table — Top 10 Items (feeds chart 4)

The clean, formula-only, no-sorting approach uses `LARGE` (the *n*-th biggest
value) plus another `XLOOKUP` to name it. Under the pre-set `Item` / `Revenue`
headers (`H5` / `I5`):

| Cell | Content |
|---|---|
| `I6` | `=LARGE(Sales_Analysis.F:F, 1)` → fill `I6:I15` becomes `LARGE(..., 1)`…`LARGE(..., 10)` |
| `H6` | `=XLOOKUP(I6, Sales_Analysis.F:F, Sales_Analysis.B:B)` → fill to `H15` |

> Alternative (lower-tech): copy `Sales_Analysis` A:F, **Paste Special → Values
> Only** into a scratch area, **Data → Sort** by Revenue descending, take the top
> 10. Teaches sort; `LARGE`+`XLOOKUP` teaches functions. Either is acceptable.

### 4d. The four charts

| # | Type | Source | Reading it |
|---|---|---|---|
| 1 | **Column (bar)** | `A5:B15` | which category earns most |
| 2 | **Line** | `D5:E11` | revenue trend across the quarter |
| 3 | **Pie** | `A5:B15` | each category's share of revenue (data labels = %) |
| 4 | **Bar (horizontal)** | `H5:I15` | the 10 best-selling items |

Each chart must have a **title** and **axis titles**; the pie needs **% data
labels**; add a **legend** only where it helps (the pie; not the single-series
column).

> **Chart-type choice is graded, not just "a chart exists":** *trend over time →
> line; parts of a whole → pie; compare categories/items → bar/column.* A pie of
> monthly revenue is the classic wrong answer.

---

## 5. Expected final numbers (for instructor verification)

From the seed in `sales.xlsx` (Indian digit grouping):

| KPI | Expected value |
|---|---|
| **Total Revenue** (`=SUM(Sales_Analysis.F:F)`) | **₹14,82,17,110** (148,217,110) |
| **Top category** by revenue | **Power Tools — ₹9,29,46,470** (62.7% of all revenue) |
| **Top-selling item** by revenue | **HW-0130 · DeWalt Bench Grinder 8 inch** — 301 units, ₹68,35,710 |
| **Busiest month** by revenue | **Mar 2026 — ₹5,18,15,790** |

Revenue by category (the column/pie chart), descending:

| Category | Revenue | Share |
|---|---|---|
| Power Tools | ₹9,29,46,470 | 62.7% |
| Hand Tools | ₹1,06,22,410 | 7.2% |
| Electrical | ₹1,05,26,360 | 7.1% |
| Paints & Coatings | ₹79,48,370 | 5.4% |
| Garden Tools | ₹62,88,420 | 4.2% |
| Hardware | ₹61,61,910 | 4.2% |
| Plumbing | ₹47,63,090 | 3.2% |
| Safety Gear | ₹44,65,000 | 3.0% |
| Adhesives & Sealants | ₹32,72,350 | 2.2% |
| Fasteners | ₹12,22,730 | 0.8% |

Monthly revenue (the line chart):

| Month | Revenue |
|---|---|
| Oct 2025 | ₹1,80,35,400 |
| Nov 2025 | ₹1,91,00,730 |
| Dec 2025 | ₹2,08,01,620 |
| Jan 2026 | ₹2,16,12,790 |
| Feb 2026 | ₹1,68,50,780 |
| Mar 2026 | ₹5,18,15,790 |

> **Instructor note — the March spike is expected.** Q1-P2's data generator adds
> end-of-period "bulk clearance" sales near the 31 Mar 2026 cut-off, so March
> revenue runs ~2.5× a normal month. It's a data artifact, not a real seasonal
> trend — the line chart will show a steady Oct→Jan climb, a Feb dip, then a sharp
> March jump. Don't let it confuse you when checking a student's line chart. (If
> you'd rather not explain it, the units-per-month variant in §4b shows the same
> shape.)

If a student's numbers diverge:
- Wrong XLOOKUP return column → Selling Price wrong → Revenue collapses.
- `XLOOKUP` arrays of different heights → `#VALUE!` or shifted results.
- Forgot the `D4*` in the Sale Value helper (price alone, not price × quantity) → monthly revenue far too low.
- Charted raw 350-row data → unreadable / wrong totals.

---

## 6. Submission

Save as `<first_name>_jugaad_sales.ods` (OpenDocument **Spreadsheet** — `.ods`,
not `.odt`; see the Q1-P2 note). Email to `hussain@cs17.org`.

---

## Common student mistakes (quick reference)

1. **Wrong chart type for the data** — pie for a time trend, line for unordered
   categories. The single most common loss of marks here.
2. **Charting raw 350-row data** instead of a summary table — unreadable.
3. **Hardcoding the summary tables** — same no-hardcoding rule as Q1-P2; every
   summary cell must be a formula.
4. **`XLOOKUP` arrays different lengths** — `lookup_array` and `return_array`
   must be the same height (`A:A` with `G:G` is fine; `A4:A353` with `G4:G400`
   is not).
5. **Two title rows** — same row-numbering trap as Q1-P2.
6. **Untitled charts / missing axis labels** — graded; a chart that doesn't
   communicate scores nothing.
