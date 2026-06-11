"""segen — seven-segment display practice-sheet generator for cs17.org.

A seven-segment display shows a digit by lighting up to seven little bars
(segments), labelled a–g. The whole display is therefore just 7 bits — one per
bar, 1 = lit, 0 = off — and the pattern of 7 bits for each digit 0–9 is the
display's truth table.

Single source of truth: each digit is authored once as the SET of segments that
light up (`display.LIT`). From that one fact we derive BOTH the 7-bit output row
(`display.bits`) AND the TikZ drawing of the lit glyph (`display.glyph`), so the
picture a student sees and the truth-table row they fill in can never disagree.

One problem kind: SEVENSEG — complete the digit → 7-bit truth table.
"""
from .display import LIT, SEGMENTS, bits, glyph, reference
from .problem import DECODER, SEVENSEG, Problem

__all__ = ["Problem", "SEVENSEG", "DECODER", "LIT", "SEGMENTS", "bits", "glyph",
           "reference"]
