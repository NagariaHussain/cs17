"""Build sales.xlsx — the seed workbook for Q1-P3 (Sales Analysis).

Q1-P3 is a focused sales + charts assignment: no stock levels, no reorder/damage
logic. We reuse Q1-P2's data so students see a familiar business, but distil it
down to just what a sales analysis needs:

  - Item_Master : product catalogue (Item ID, Name, Category, Brand, Unit,
                  Cost Price, Selling Price) — the stock columns (Supplier ID,
                  Reorder Level, Opening Stock) are dropped.
  - Sales       : one row per sale — only the OUT transactions from Q1-P2's
                  Stock_Transactions, renumbered SALE-#####. No IN / DAMAGE /
                  RETURN movements (those are stock, not sales).
  - Sales_Analysis : Item ID column pre-filled, headers present — students build it.
  - Charts      : blank — students build it.

    python build_seed.py        # writes references/sales.xlsx
"""
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

HERE = Path(__file__).resolve().parent
Q1P2 = HERE.parent / "q1-p2_jugaad_inventory" / "references" / "stock.xlsx"
OUT_PATH = str(HERE / "references" / "sales.xlsx")

if not Q1P2.exists():
    raise SystemExit(
        f"Q1-P2 seed not found at {Q1P2}\n"
        "Run `python build_seed.py` in ../q1-p2_jugaad_inventory first."
    )

src = load_workbook(Q1P2, data_only=True)

# ─── Read the bits we keep from Q1-P2 ────────────────────────────────────────
# Item_Master layout in Q1-P2: A Item ID, B Name, C Category, D Brand, E Unit,
# F Supplier ID, G Cost Price, H Selling Price, I Reorder Level, J Opening Stock.
src_im = src["Item_Master"]
items = []
for r in src_im.iter_rows(min_row=2, values_only=True):
    if r[0] is None:
        continue
    items.append({
        "Item ID": r[0], "Item Name": r[1], "Category": r[2], "Brand": r[3],
        "Unit": r[4], "Cost Price": r[6], "Selling Price": r[7],
    })

# Stock_Transactions: A Txn ID, B Date, C Item ID, D Type, E Qty, F Reference, G Notes.
# Keep only OUT rows = actual sales.
src_tx = src["Stock_Transactions"]
sales = []
for r in src_tx.iter_rows(min_row=2, values_only=True):
    if r[0] is None or r[3] != "OUT":
        continue
    sales.append({"Date": r[1], "Item ID": r[2], "Quantity": r[4], "Invoice No": r[5]})
sales.sort(key=lambda s: s["Date"])
for n, s in enumerate(sales, start=1):
    s["Sale ID"] = f"SALE-{n:05d}"

# ─── Build the focused workbook ──────────────────────────────────────────────
wb = Workbook()
wb.remove(wb.active)
im = wb.create_sheet("Item_Master")
sl = wb.create_sheet("Sales")
sa = wb.create_sheet("Sales_Analysis")
ch = wb.create_sheet("Charts")

im_cols = ["Item ID", "Item Name", "Category", "Brand", "Unit", "Cost Price", "Selling Price"]
im.append(im_cols)
for it in items:
    im.append([it[c] for c in im_cols])

sl_cols = ["Sale ID", "Date", "Item ID", "Quantity", "Invoice No"]
sl.append(sl_cols)
for s in sales:
    sl.append([s[c] for c in sl_cols])

# Sales_Analysis: header row + the Item IDs to analyse (rest are student formulas).
sa_cols = ["Item ID", "Item Name", "Category", "Units Sold", "Selling Price", "Revenue"]
sa.append(sa_cols)
for it in items:
    sa.append([it["Item ID"]])

# ─── Styling: lime headers, frozen header row, sensible widths ───────────────
header_font = Font(name="Arial", bold=True, color="FFFFFF", size=11)
header_fill = PatternFill("solid", start_color="5B8C00")
header_align = Alignment(horizontal="center", vertical="center")
thin = Side(border_style="thin", color="BFBFBF")
header_border = Border(left=thin, right=thin, top=thin, bottom=thin)

for ws in (im, sl, sa):
    for cell in ws[1]:
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        cell.border = header_border
    ws.row_dimensions[1].height = 22
    ws.freeze_panes = "A2"
    for col_cells in ws.iter_cols(min_row=1, max_row=min(ws.max_row, 50)):
        max_len = max((len(str(c.value)) for c in col_cells if c.value is not None), default=10)
        ws.column_dimensions[col_cells[0].column_letter].width = min(max_len + 4, 32)

# ─── Charts sheet: pre-laid-out skeleton students fill in ────────────────────
# Three empty summary tables, each with a styled section title + headers, so
# students focus on the formulas + charts, not the layout. (This sheet ships
# with its title bar done, so — unlike the other three — students do NOT insert
# title rows here.) Data cells are intentionally left blank.
ch.merge_cells("A1:I2")
title = ch["A1"]
title.value = "Charts: Jugaad Hardware & Tools"
title.font = Font(name="Arial", bold=True, color="FFFFFF", size=16)
title.fill = PatternFill("solid", start_color="000000")
title.alignment = Alignment(horizontal="center", vertical="center")
ch.row_dimensions[1].height = 18
ch.row_dimensions[2].height = 18

# (left col, right col, section title, header 1, header 2, left-col width)
sections = [
    ("A", "B", "Revenue by Category", "Category", "Revenue", 26),
    ("D", "E", "Monthly Revenue", "Month", "Revenue", 14),
    ("H", "I", "Top 10 Items by Revenue", "Item", "Revenue", 34),
]
sec_font = Font(name="Arial", bold=True, color="2E4600", size=12)
sec_fill = PatternFill("solid", start_color="D6E9B0")          # light lime accent
sec_align = Alignment(horizontal="center", vertical="center")
sec_underline = Side(border_style="medium", color="5B8C00")    # the "underscore"
for c1, c2, sec_title, h1, h2, w1 in sections:
    ch.merge_cells(f"{c1}4:{c2}4")
    st = ch[f"{c1}4"]
    st.value, st.font, st.fill, st.alignment = sec_title, sec_font, sec_fill, sec_align
    for addr in (f"{c1}4", f"{c2}4"):
        ch[addr].border = Border(bottom=sec_underline)
    for addr, val in ((f"{c1}5", h1), (f"{c2}5", h2)):
        hc = ch[addr]
        hc.value, hc.font, hc.fill, hc.alignment, hc.border = (
            val, header_font, header_fill, header_align, header_border)
    ch.column_dimensions[c1].width = w1
    ch.column_dimensions[c2].width = 16

wb.save(OUT_PATH)
print(f"Built {OUT_PATH}: {len(items)} items, {len(sales)} sales | sheets: {wb.sheetnames}")
