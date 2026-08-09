"""papergen — graded question papers for cs17.org.

The worksheet generators model a *topic* (an expression, an algorithm, a Scratch
script) and derive a practice sheet from it. A paper is a different object: it
has sections, a marks budget that has to add up, and exam chrome (duration,
maximum marks, general instructions). papergen supplies that structure, and
keeps the worksheets' single-source habit where there is something to derive —
a Calc question's tables are authored once as a `Workbook` and every figure on
the answer key is computed from them (`sheet.py`).

Scratch answers are drawn by scratchgen's own renderer, so a paper's model
solution and the build-along worksheets show identical blocks.
"""

from .paper import Paper, Section, Question, Part, SheetTable, Cell
from .sheet import Product, Sale, Row, Workbook, Pivot, rupees, plain
from .latex import fx

__all__ = [
    "Paper", "Section", "Question", "Part", "SheetTable", "Cell",
    "Product", "Sale", "Row", "Workbook", "Pivot", "rupees", "plain", "fx",
]
