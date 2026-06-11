"""Worksheet 5 — the seven-segment display as a 7-bit truth table.

One focused question: a seven-segment display is really just 7 bits (one per
bar, a–g). The student works out which bars light up for each digit 0–9 and
writes the seven output bits — that table IS the display's truth table.

Authored once from the single source of truth in segen.display: each digit's
lit segments drive both the glyph drawing and the bit row, so the picture and
the answer can never disagree.
"""

from gens.segen import DECODER, SEVENSEG

TITLE = "Worksheet 5"

PROBLEMS = [
    # Problem 1: digit (shown as a numeral) -> which 7 bars light up.
    SEVENSEG(
        example=7,
        note="Hint: it helps to picture the digit on the display first, then "
             "tick off each of the seven bars in turn.",
    ),
    # Problem 2: the expansion — the digit now arrives as a binary number too,
    # so the table is binary-in / binary-out (the full seven-segment decoder).
    DECODER(tag="Advanced"),
]
