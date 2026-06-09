"""Binary numbers — the single source of truth for a binary worksheet problem.

Two skills:
  - convert a binary number to decimal   (place values)
  - decode a message from ASCII codes     (binary -> decimal -> character)

The binary string is the source for a conversion problem (its width is exactly
what the student sees). The plaintext message is the source for a decode problem
— each character's ASCII code, in `width`-bit binary, is derived from it, so the
codes the student sees and the answer can never disagree.
"""

from __future__ import annotations

# Control-character mnemonics: code -> short name (codes 0..31). Printable codes
# (33..126) render as the character itself; 32 and 127 get the conventional
# SP / DEL. This is the single source for the ASCII reference table.
_CONTROL = [
    "NUL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL",
    "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI",
    "DLE", "DC1", "DC2", "DC3", "DC4", "NAK", "SYN", "ETB",
    "CAN", "EM", "SUB", "ESC", "FS", "GS", "RS", "US",
]


def ascii_label(code: int) -> str:
    """The label shown in the ASCII reference table for `code` (0..127)."""
    if code < 32:
        return _CONTROL[code]
    if code == 32:
        return "SP"
    if code == 127:
        return "DEL"
    return chr(code)


def to_binary(n: int, width: int = 8) -> str:
    return format(n, f"0{width}b")


def from_binary(bits: str) -> int:
    return int(bits, 2)


def place_values(bits: str) -> list[tuple[str, int]]:
    """Each bit (most-significant first) paired with its place value."""
    n = len(bits)
    return [(b, 1 << (n - 1 - i)) for i, b in enumerate(bits)]


def expansion(bits: str) -> tuple[list[int], int]:
    """Place-value working: the contributing values (the 1-bits) and the total.
    e.g. '1011' -> ([8, 2, 1], 11)."""
    contribs = [v for b, v in place_values(bits) if b == "1"]
    return contribs, from_binary(bits)


def encode(message: str, width: int = 8) -> list[tuple[str, int, str]]:
    """Each character -> (binary code, decimal code, character)."""
    return [(to_binary(ord(c), width), ord(c), c) for c in message]
