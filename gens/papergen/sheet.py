"""The workbook behind a Calc question — the single source of truth.

A practical Calc question hands the student two tables and then asks for figures
derived from them: lookups, an amount column, totals, SUMIFS answers, a
region summary, a pivot. Author the two tables once here and *every* number the
answer key prints is computed from them, so editing a unit price or a quantity
can never leave the key quoting a stale total.

The spreadsheet row number of each record is derived too (`Row.excel_row`), so
the cell references in the question text and on the key stay correct if a record
is added or removed.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Product:
    """One row of the Product_Master sheet."""
    code: str
    name: str
    category: str
    price: float


@dataclass(frozen=True)
class Sale:
    """One order in the Sales_Data register — it stores only the product code."""
    order: str
    date: str
    code: str
    region: str
    qty: int


@dataclass(frozen=True)
class Row:
    """A sales record with the looked-up columns filled in — i.e. what the
    student's sheet should look like once columns F-I hold their formulas."""
    sale: Sale
    product: Product
    excel_row: int

    @property
    def name(self) -> str:
        return self.product.name

    @property
    def category(self) -> str:
        return self.product.category

    @property
    def price(self) -> float:
        return self.product.price

    @property
    def amount(self) -> float:
        return self.sale.qty * self.product.price


@dataclass(frozen=True)
class Pivot:
    """Region x Category sums with both margins — the expected pivot table."""
    regions: tuple
    categories: tuple
    cells: dict            # (region, category) -> amount
    row_totals: dict       # region -> amount
    col_totals: dict       # category -> amount
    grand_total: float

    def cell(self, region: str, category: str) -> float:
        return self.cells[(region, category)]


class Workbook:
    """The two sheets plus every figure derived from them.

    `regions` and `categories` fix the display order used by the summary table
    and the pivot; both default to the order the values first appear in the data.
    """

    HEADER_ROWS = 1        # both sheets have one header row, so data starts at 2

    def __init__(self, products, sales, *, regions=None, categories=None):
        self.products = tuple(products)
        self.sales = tuple(sales)
        self._by_code = {p.code: p for p in self.products}

        missing = sorted({s.code for s in self.sales} - set(self._by_code))
        assert not missing, f"sales reference unknown product codes: {missing}"

        self.regions = tuple(regions) if regions else self._first_seen(
            s.region for s in self.sales)
        self.categories = tuple(categories) if categories else self._first_seen(
            self._by_code[s.code].category for s in self.sales)

    @staticmethod
    def _first_seen(values) -> tuple:
        return tuple(dict.fromkeys(values))

    # ---- the sheets ---------------------------------------------------------

    @property
    def rows(self) -> list[Row]:
        """Sales_Data with columns F-I resolved."""
        return [Row(s, self._by_code[s.code], i)
                for i, s in enumerate(self.sales, self.HEADER_ROWS + 1)]

    @property
    def first_data_row(self) -> int:
        return self.HEADER_ROWS + 1

    @property
    def last_data_row(self) -> int:
        return self.HEADER_ROWS + len(self.sales)

    @property
    def last_product_row(self) -> int:
        return self.HEADER_ROWS + len(self.products)

    # ---- the derived figures ------------------------------------------------

    def grand_total(self) -> float:
        return sum(r.amount for r in self.rows)

    def average_order(self) -> float:
        return self.grand_total() / len(self.sales)

    def highest_order(self) -> float:
        return max(r.amount for r in self.rows)

    def highest_row(self) -> Row:
        return max(self.rows, key=lambda r: r.amount)

    def sumifs(self, *, category=None, region=None, name=None) -> float:
        """The SUMIFS the student writes, evaluated here — same criteria, so the
        key's number is whatever their correct formula would return."""
        return sum(r.amount for r in self.rows
                   if (category is None or r.category == category)
                   and (region is None or r.sale.region == region)
                   and (name is None or r.name == name))

    def by_region(self) -> dict:
        return {reg: self.sumifs(region=reg) for reg in self.regions}

    def by_category(self) -> dict:
        return {cat: self.sumifs(category=cat) for cat in self.categories}

    def top_region(self) -> tuple:
        """(region, amount) for the region with the highest total sales."""
        return max(self.by_region().items(), key=lambda kv: kv[1])

    def pivot(self) -> Pivot:
        cells = {(reg, cat): self.sumifs(region=reg, category=cat)
                 for reg in self.regions for cat in self.categories}
        return Pivot(regions=self.regions, categories=self.categories, cells=cells,
                     row_totals=self.by_region(), col_totals=self.by_category(),
                     grand_total=self.grand_total())


# ---- formatting helpers -------------------------------------------------------

def rupees(v: float) -> str:
    """A Currency (Rs.) value with 2 decimals — the format column I is asked to
    carry, so the key shows the figure exactly as the student's cell should."""
    return f"Rs. {v:,.2f}"


def plain(v: float) -> str:
    """A bare number with thousands separators (no currency symbol)."""
    return f"{v:,.0f}" if float(v).is_integer() else f"{v:,.2f}"
