"""Pixel bitmaps — a black-and-white picture is a grid of bits, one byte per row.

A bitmap is authored once as ASCII art (rows of '#'/'.'); from it we derive each
row's bits, its hexadecimal byte, and the rendered image — so the hex the student
converts and the picture that appears can never disagree. This is the real-world
tie-together: an image is just numbers.
"""

from __future__ import annotations

_ON = {"#", "1", "X", "x", "*", "█"}  # any of these mean a filled pixel


def to_bits(row: str) -> list[int]:
    return [1 if ch in _ON else 0 for ch in row]


def row_bin(bits: list[int]) -> str:
    return "".join(str(b) for b in bits)


def row_hex(bits: list[int]) -> str:
    """The row's byte(s) in hex, zero-padded to cover its width (8 px -> 2 digits)."""
    value = int(row_bin(bits) or "0", 2)
    return format(value, "0%dX" % ((len(bits) + 3) // 4))
