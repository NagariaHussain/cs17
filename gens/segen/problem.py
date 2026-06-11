"""A seven-segment worksheet problem.

  SEVENSEG  complete the digit -> 7-bit (segments a–g) truth table
  DECODER   binary input (the digit) -> 7-bit output: the full decoder table

SEVENSEG: the student works out which bars light up for each digit and writes
the 7 output bits; `example` is the one digit shown fully worked as the method.

DECODER expands it — the digit now arrives as a binary number too, so the table
is binary-in / binary-out (the classic seven-segment decoder). The student first
reasons out how many input bits are needed for 0–9, then fills the table.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .display import LIT

KINDS = ("sevenseg", "decoder")


@dataclass
class Problem:
    kind: str = "sevenseg"
    digits: list = field(default_factory=lambda: list(range(10)))
    example: int = 7
    tag: str = ""         # optional difficulty badge shown by the heading (e.g. "Advanced")
    note: str = ""
    description: str = ""

    def __post_init__(self):
        assert self.kind in KINDS, f"unknown kind {self.kind!r}"
        for d in self.digits:
            assert d in LIT, f"no seven-segment pattern for digit {d!r}"
        assert self.example in LIT, f"no pattern for example digit {self.example!r}"


def SEVENSEG(digits=None, *, example: int = 7, tag: str = "", note: str = "",
             description: str = "") -> Problem:
    """Complete the seven-segment truth table for `digits` (default 0–9). One
    `example` digit is shown fully worked first as the method."""
    return Problem(digits=list(range(10)) if digits is None else list(digits),
                   example=example, tag=tag, note=note, description=description)


def DECODER(digits=None, *, tag: str = "", note: str = "",
            description: str = "") -> Problem:
    """The full decoder truth table: each digit is given in decimal, written as a
    binary INPUT (enough bits to count 0–9), and the seven segment bits a–g are
    the OUTPUT. `tag` shows an optional difficulty badge (e.g. "Advanced")."""
    return Problem("decoder", digits=list(range(10)) if digits is None else list(digits),
                   tag=tag, note=note, description=description)
