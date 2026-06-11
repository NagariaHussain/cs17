"""Build jugaad_sales_answers.xlsx — the model solution for Q1-P3.

Same data as the student seed (sales.xlsx), but fully worked: the two title rows
are in place (headers on row 3, data from row 4), and EVERY formula is filled in
exactly as the README answer key specifies —

  - Sales_Analysis : Item Name / Category / Selling Price (XLOOKUP), Units Sold
                     (SUMIFS), Revenue (= units x price).
  - Sales          : the two helper columns — Sale Value (XLOOKUP x qty) and Month.
  - Charts         : all three summary tables filled (category list + SUMIFS,
                     month list + SUMIFS, LARGE + XLOOKUP top-10).

The only thing left to do by hand is **insert the four chart objects** — formula
engines can't be scripted into a chart via openpyxl in a way LibreOffice reads
cleanly, and chart styling is exactly what the assignment is testing anyway.

Notes:
  - This is an .xlsx, so cross-sheet refs use Excel's `!` (the student .ods uses
    `.`). XLOOKUP is stored with the `_xlfn.` prefix so both Excel and LibreOffice
    recognise it; they display it as plain `XLOOKUP`.
  - openpyxl writes formulas, not their results — open in Calc/Excel and accept
    the "recalculate" prompt to see the numbers. Expected total revenue:
    148,217,110.

    python build_answer_key.py        # writes references/jugaad_sales_answers.xlsx
"""
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HERE = Path(__file__).resolve().parent
Q1P2 = HERE.parent / "q1-p2_jugaad_inventory" / "references" / "stock.xlsx"
OUT_PATH = str(HERE / "references" / "jugaad_sales_answers.xlsx")
XL = "_xlfn.XLOOKUP"   # XLOOKUP, stored so Excel + LibreOffice both accept it
RUPEE = u'₹#,##,##0'   # Indian digit grouping

if not Q1P2.exists():
    raise SystemExit(f"Q1-P2 seed not found at {Q1P2} — build it first.")

# ─── Read the same data the seed uses ────────────────────────────────────────
src = load_workbook(Q1P2, data_only=True)
items = []
for r in src["Item_Master"].iter_rows(min_row=2, values_only=True):
    if r[0] is None:
        continue
    items.append({"Item ID": r[0], "Item Name": r[1], "Category": r[2],
                  "Brand": r[3], "Unit": r[4], "Cost Price": r[6], "Selling Price": r[7]})
sales = []
for r in src["Stock_Transactions"].iter_rows(min_row=2, values_only=True):
    if r[0] is None or r[3] != "OUT":
        continue
    sales.append({"Date": r[1], "Item ID": r[2], "Quantity": r[4], "Invoice No": r[5]})
sales.sort(key=lambda s: s["Date"])
for n, s in enumerate(sales, start=1):
    s["Sale ID"] = f"SALE-{n:05d}"

# Category list in the README's order (validated against the data below).
CATEGORIES = ["Power Tools", "Hand Tools", "Hardware", "Fasteners", "Electrical",
              "Plumbing", "Paints & Coatings", "Adhesives & Sealants",
              "Safety Gear", "Garden Tools"]
assert set(CATEGORIES) == {it["Category"] for it in items}, "category list mismatch"
MONTHS = ["Oct 2025", "Nov 2025", "Dec 2025", "Jan 2026", "Feb 2026", "Mar 2026"]

# ─── Styles ──────────────────────────────────────────────────────────────────
title_font = Font(name="Arial", bold=True, color="FFFFFF", size=16)
title_fill = PatternFill("solid", start_color="000000")
center = Alignment(horizontal="center", vertical="center")
hdr_font = Font(name="Arial", bold=True, color="FFFFFF", size=11)
hdr_fill = PatternFill("solid", start_color="5B8C00")
thin = Side(border_style="thin", color="BFBFBF")
hdr_border = Border(left=thin, right=thin, top=thin, bottom=thin)
sec_font = Font(name="Arial", bold=True, color="2E4600", size=12)
sec_fill = PatternFill("solid", start_color="D6E9B0")
sec_underline = Side(border_style="medium", color="5B8C00")


def title_bar(ws, text):
    ws.merge_cells("C1:D2")
    c = ws["C1"]
    c.value, c.font, c.fill, c.alignment = text, title_font, title_fill, center


def header_row(ws, cols, row=3):
    for i, name in enumerate(cols, start=1):
        c = ws.cell(row, i, name)
        c.font, c.fill, c.alignment, c.border = hdr_font, hdr_fill, center, hdr_border
    ws.freeze_panes = ws.cell(row + 1, 1).coordinate


wb = Workbook()
wb.remove(wb.active)
im = wb.create_sheet("Item_Master")
sl = wb.create_sheet("Sales")
sa = wb.create_sheet("Sales_Analysis")
ch = wb.create_sheet("Charts")

# ─── Item_Master (data only) ─────────────────────────────────────────────────
im_cols = ["Item ID", "Item Name", "Category", "Brand", "Unit", "Cost Price", "Selling Price"]
title_bar(im, "Items: Jugaad Hardware & Tools")
header_row(im, im_cols)
for k, it in enumerate(items):
    r = 4 + k
    for i, col in enumerate(im_cols, start=1):
        im.cell(r, i, it[col])
    im.cell(r, 6).number_format = RUPEE
    im.cell(r, 7).number_format = RUPEE

# ─── Sales (data + the two helper columns as formulas) ───────────────────────
sl_cols = ["Sale ID", "Date", "Item ID", "Quantity", "Invoice No", "Sale Value", "Month"]
title_bar(sl, "Sales: Jugaad Hardware & Tools")
header_row(sl, sl_cols)
for k, s in enumerate(sales):
    r = 4 + k
    sl.cell(r, 1, s["Sale ID"])
    sl.cell(r, 2, s["Date"]).number_format = "yyyy-mm-dd"
    sl.cell(r, 3, s["Item ID"])
    sl.cell(r, 4, s["Quantity"])
    sl.cell(r, 5, s["Invoice No"])
    sl.cell(r, 6, f"=D{r}*{XL}(C{r},Item_Master!A:A,Item_Master!G:G)").number_format = RUPEE
    sl.cell(r, 7, f'=TEXT(B{r},"MMM YYYY")')

# ─── Sales_Analysis (every column a formula except Item ID) ──────────────────
sa_cols = ["Item ID", "Item Name", "Category", "Units Sold", "Selling Price", "Revenue"]
title_bar(sa, "Sales Analysis: Jugaad Hardware & Tools")
header_row(sa, sa_cols)
for k, it in enumerate(items):
    r = 4 + k
    sa.cell(r, 1, it["Item ID"])
    sa.cell(r, 2, f"={XL}(A{r},Item_Master!A:A,Item_Master!B:B)")
    sa.cell(r, 3, f"={XL}(A{r},Item_Master!A:A,Item_Master!C:C)")
    sa.cell(r, 4, f"=SUMIFS(Sales!D:D,Sales!C:C,A{r})")
    sa.cell(r, 5, f"={XL}(A{r},Item_Master!A:A,Item_Master!G:G)").number_format = RUPEE
    sa.cell(r, 6, f"=D{r}*E{r}").number_format = RUPEE

# ─── Charts: title bar + three filled summary tables ─────────────────────────
ch.merge_cells("A1:I2")
ch["A1"].value, ch["A1"].font, ch["A1"].fill, ch["A1"].alignment = (
    "Charts: Jugaad Hardware & Tools", title_font, title_fill, center)

# (left, right, title, h1, h2, left-width)
sections = [("A", "B", "Revenue by Category", "Category", "Revenue", 26),
            ("D", "E", "Monthly Revenue", "Month", "Revenue", 14),
            ("H", "I", "Top 10 Items by Revenue", "Item", "Revenue", 34)]
for c1, c2, sec_title, h1, h2, w1 in sections:
    ch.merge_cells(f"{c1}4:{c2}4")
    st = ch[f"{c1}4"]
    st.value, st.font, st.fill, st.alignment = sec_title, sec_font, sec_fill, center
    for a in (f"{c1}4", f"{c2}4"):
        ch[a].border = Border(bottom=sec_underline)
    for a, v in ((f"{c1}5", h1), (f"{c2}5", h2)):
        x = ch[a]
        x.value, x.font, x.fill, x.alignment, x.border = v, hdr_font, hdr_fill, center, hdr_border
    ch.column_dimensions[c1].width = w1
    ch.column_dimensions[c2].width = 16

# Revenue by Category (A6:B15)
for k, cat in enumerate(CATEGORIES):
    r = 6 + k
    ch.cell(r, 1, cat)
    ch.cell(r, 2, f"=SUMIFS(Sales_Analysis!F:F,Sales_Analysis!C:C,A{r})").number_format = RUPEE
# Monthly Revenue (D6:E11)
for k, mon in enumerate(MONTHS):
    r = 6 + k
    ch.cell(r, 4, mon)
    ch.cell(r, 5, f"=SUMIFS(Sales!F:F,Sales!G:G,D{r})").number_format = RUPEE
# Top 10 Items (H6:I15) — LARGE picks the nth revenue, XLOOKUP names it
for k in range(10):
    r = 6 + k
    ch.cell(r, 9, f"=LARGE(Sales_Analysis!F:F,{k + 1})").number_format = RUPEE
    ch.cell(r, 8, f"={XL}(I{r},Sales_Analysis!F:F,Sales_Analysis!B:B)")

# ─── Widths for the data sheets ──────────────────────────────────────────────
for ws, widths in ((im, [10, 34, 20, 14, 8, 12, 14]),
                   (sl, [12, 13, 10, 10, 12, 14, 12]),
                   (sa, [10, 34, 20, 12, 14, 14])):
    for i, w in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = w

wb.save(OUT_PATH)
print(f"Built {OUT_PATH}")
print(f"  Item_Master   : {len(items)} items (rows 4-{3+len(items)})")
print(f"  Sales         : {len(sales)} sales + Sale Value/Month helpers (rows 4-{3+len(sales)})")
print(f"  Sales_Analysis: {len(items)} rows of formulas (rows 4-{3+len(items)})")
print(f"  Charts        : 3 summary tables filled — insert the 4 charts by hand")
