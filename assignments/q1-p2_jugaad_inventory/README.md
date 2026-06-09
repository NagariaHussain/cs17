# Q1-P2 — Jugaad Hardware Inventory: Walkthrough & Solutions

Reference solution for [`/student-handbook/assignments/q1-p2`](https://portal.cs17.org/student-handbook/assignments/q1-p2).

> **This folder (prep, not the published assignment).** The student-facing
> assignment is hand-written markdown on the wiki (link above). What lives here:
> - `build_seed.py` — regenerates `references/stock.xlsx` from scratch (`python build_seed.py`).
> - `references/stock.xlsx` — the seed workbook students start from.
> - `references/jugaad_inventory.ods` — the completed model solution.
> - this file — the instructor walkthrough / answer key.

> All formulas use LibreOffice's sheet-reference style (`.`). If a student is on Excel they can swap `.` for `!` and the formulas still work.
>
> After step 1 every sheet gains **two title rows on top**, so column headers move to **row 3** and data starts at **row 4**. Every cell reference below already accounts for this.

---

## 1. Basics — Sheet titles

Do this for **every sheet**:

1. Right-click row 1 header → **Insert Rows Above** → repeat once (now rows 1 & 2 are blank).
2. Select `C1:D2` → toolbar **Merge and Center Cells** (or `Format → Merge Cells → Merge Cells`).
3. Type the title:
   - `Item_Master` → `Items: Jugaad Hardware & Tools`
   - `Suppliers` → `Supplier: Jugaad Hardware & Tools`
   - `Stock_Transactions` → `Stock Transactions: Jugaad Hardware & Tools`
   - `Current_Stock` → `Current Stock: Jugaad Hardware & Tools`
   - `Dashboard` → `Dashboard: Jugaad Hardware & Tools`
4. With the merged cell still selected: **Format → Cells…** (`Ctrl+1`)
   - **Background** tab → pick black
   - **Font** tab → colour white, size 16
   - **Alignment** tab → Horizontal **Center**, Vertical **Middle**

> **Vertical centering hint:** it's under the Alignment tab, not the Format toolbar — that toolbar only does horizontal alignment by default.

---

## 2. Current_Stock — Phase 1 (lookups)

The `Item ID` column is already populated from `A4:A353`. For each of the remaining lookup columns, write the formula in **row 4** and fill down to **row 353**.

| Target column | Cell | Formula |
|---|---|---|
| Item Name | `B4` | `=VLOOKUP(A4, Item_Master.A:J, 2, 0)` |
| Category | `C4` | `=VLOOKUP(A4, Item_Master.A:J, 3, 0)` |
| Opening Stock | `D4` | `=VLOOKUP(A4, Item_Master.A:J, 10, 0)` |
| Unit Cost | `J4` | `=VLOOKUP(A4, Item_Master.A:J, 7, 0)` |
| Reorder Level | `L4` | `=VLOOKUP(A4, Item_Master.A:J, 9, 0)` |

The fourth argument (`0` or `FALSE`) forces an **exact match** — without it, VLOOKUP does a fuzzy match against a sorted list and you get wrong answers.

> Column numbers come from `Item_Master`'s layout: A=Item ID, B=Item Name, C=Category, D=Brand, E=Unit, F=Supplier ID, G=Cost Price, H=Selling Price, I=Reorder Level, J=Opening Stock.

---

## 3. Current_Stock — Phase 2 (SUMIFS aggregations)

| Target column | Cell | Formula |
|---|---|---|
| Total Purchased | `E4` | `=SUMIFS(Stock_Transactions.E:E, Stock_Transactions.C:C, A4, Stock_Transactions.D:D, "IN")` |
| Total Sold | `F4` | `=SUMIFS(Stock_Transactions.E:E, Stock_Transactions.C:C, A4, Stock_Transactions.D:D, "OUT")` |
| Damaged Qty | `G4` | `=SUMIFS(Stock_Transactions.E:E, Stock_Transactions.C:C, A4, Stock_Transactions.D:D, "DAMAGE")` |
| Returned Qty | `H4` | `=SUMIFS(Stock_Transactions.E:E, Stock_Transactions.C:C, A4, Stock_Transactions.D:D, "RETURN")` |
| Current Stock | `I4` | `=D4+E4-F4-G4+H4` |
| Stock Value | `K4` | `=I4*J4` |

### Why `SUMIFS` not `SUMIF`?
`SUMIF` takes a single condition. Here every per-item total needs **two** filters — match the `Item ID` *and* match the transaction `Type`. The extra `S` in `SUMIFS` is the multi-criteria version.

Same rule of thumb: `COUNTIF`/`AVERAGEIF` for one condition, `COUNTIFS`/`AVERAGEIFS` for two or more.

---

## 4. Stock Status — `IFS`

`M4`:
```
=IFS(I4<=0, "Out of Stock", I4<=L4, "Reorder", TRUE, "OK")
```

Fill down to `M353`.

**Order matters.** The `≤ 0` check must come first — a zero stock would also pass `≤ Reorder Level`, so flipping the conditions silently mis-tags every out-of-stock item as "Reorder."

The final `TRUE, "OK"` is the catch-all that mimics an "else" branch — `IFS` returns `#N/A` if no condition matches, so always include it.

---

## 5. Conditional Formatting

### Stock Status — traffic-light styles
Select `M4:M353` → **Format → Conditional → Condition…**

| Condition | Apply style |
|---|---|
| Cell value is equal to `"Out of Stock"` | **Error** (red) |
| Cell value is equal to `"Reorder"` | **Warning** (amber) |
| Cell value is equal to `"OK"` | **Good** (green) |

### Stock Value — Data Bar
Select `K4:K353` → **Format → Conditional → Data Bar…** → accept defaults (or pick a green fill). The longest bars immediately tell Jaggu Uncle which SKUs are tying up the most capital.

---

## 6. Dashboard

Each KPI is two cells: a **label** (Accent 3 style) and a **value** (formula, larger merged cell, styled).

### Total Items
| Cell | Content | Style |
|---|---|---|
| `B4` | `Total Items` | Accent 3 |
| `B5:B6` (merged) | `=COUNTA(Item_Master.A:A) - 1` | Heading 1, centered H+V |

`COUNTA` of column A counts the `Item ID` header (row 3) plus all 350 data rows = 351; subtract 1 for the header.

> Alternative (more robust to header changes): `=COUNTIF(Item_Master.A:A, "HW-*")` — counts only cells that actually look like an Item ID. The assignment hint says to use `COUNTA`, but it's worth mentioning the wildcard approach as the production-grade version.

### Total Stock Value
| Cell | Content | Style |
|---|---|---|
| `D4:E4` (merged) | `Total Stock Value` | Accent 3 |
| `D5:E6` (merged) | `=SUM(Current_Stock.K:K)` | Heading 1, INR currency, centered H+V |

For INR currency: **Format → Cells → Numbers → Currency → INR ₹ English (India)** (format code `[$₹-449]#,##0;-[$₹-449]#,##0`).

### Items to Reorder
| Cell | Content | Style |
|---|---|---|
| `B10` | `Items to reorder` | Accent 3 |
| `B11` | `=COUNTIF(Current_Stock.M:M, "Reorder")` | Neutral |

### Out of Stock
| Cell | Content | Style |
|---|---|---|
| `C10` | `Out of stock` | Accent 3 |
| `C11` | `=COUNTIF(Current_Stock.M:M, "Out of Stock")` | Error |

---

## 7. Expected final numbers (for instructor verification)

Using the seed data shipped in `stock.xlsx`:

| KPI | Expected value |
|---|---|
| Total Items | **350** |
| Total Stock Value | **₹10,38,03,150** (₹103,803,150) |
| Items to Reorder | **45** |
| Out of Stock | **24** |
| OK items (implied) | **281** |

If a student's numbers diverge:
- Wrong VLOOKUP column index → Opening Stock or Unit Cost is off, Stock Value collapses
- `SUMIF` instead of `SUMIFS` → totals balloon (no Item ID filter)
- Missing the catch-all `TRUE` in `IFS` → some Stock Status cells show `#N/A`
- Conditional CF rule order flipped → Out-of-Stock rows show amber

---

## 8. Submission

> The page says rename to `<first_name>_jugaad_inventory.odt`. `.odt` is OpenDocument **Text** — for a Calc spreadsheet the correct extension is `.ods`. Check with the student / fix the assignment text. (Saving a Calc file as `.odt` will either reject the save or strip everything to a text doc.)

Email to `hussain@cs17.org`.

---

## Common student mistakes (quick reference)

1. **Adding only 1 title row instead of 2** — breaks every formula's row numbering. Catch this early.
2. **Quoting the comparison**: `=IF("I4<=0", ...)` returns `#VALUE!` because `"I4<=0"` is literal text, not a condition. Quotes belong on output values and text-match criteria, never on the logical expression itself.
3. **Forgetting the `0`/`FALSE` in VLOOKUP** — fuzzy match returns wrong items for unsorted data.
4. **Using `SUMIF` instead of `SUMIFS`** in Phase 2 (covered above).
5. **Hardcoding numbers in the Dashboard** — explicitly forbidden by the assignment. Every cell must be a formula.
