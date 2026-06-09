"""Number-base conversions (binary / decimal / hexadecimal).

A value is just an integer; each base knows how to parse and format it. A CONVERT
problem gives the student a list of values written in one base and asks for them
in another. Everything on the answer key — the target representation and the
one-line working — is derived from that same integer, so they can't disagree.
"""

from __future__ import annotations

_RADIX = {"bin": 2, "dec": 10, "hex": 16}
BASE_NAME = {"bin": "binary", "dec": "decimal", "hex": "hexadecimal"}


def parse_value(v, base: str) -> int:
    """Parse a value written in `base` (a string, or an int for decimal)."""
    return int(v) if base == "dec" else int(str(v), _RADIX[base])


def format_value(n: int, base: str) -> str:
    return {"bin": format(n, "b"), "hex": format(n, "X"), "dec": str(n)}[base]


def tex_value(s: str, base: str) -> str:
    """A value typeset with the right font and base subscript."""
    if base == "dec":
        return f"${s}$"
    return r"\texttt{%s}$_{%s}$" % (s, {"bin": "2", "hex": "16"}[base])


def _place_terms(s: str, radix: int) -> str:
    """A digit×place-value sum over the nonzero digits, e.g. '1 \\times 16 + 10'."""
    last = len(s) - 1
    terms = []
    for i, ch in enumerate(s):
        d = int(ch, radix)
        if d == 0:
            continue
        place = radix ** (last - i)
        terms.append(rf"{d} \times {place}" if place != 1 else f"{d}")
    return " + ".join(terms) if terms else "0"


def _nibbles(bits: str) -> list[str]:
    """Split a binary string into 4-bit groups, left-padding the top group."""
    bits = "0" * ((-len(bits)) % 4) + bits
    return [bits[i:i + 4] for i in range(0, len(bits), 4)]


def working(value, frm: str, to: str) -> str:
    """A LaTeX 'middle step' for converting `value` from base `frm` to `to`
    (without the leading source or trailing target). Empty if none is helpful.

      hex/bin -> dec : place-value sum            (1 \\times 16 + 10)
      bin     -> hex : group bits into nibbles    (0001\\,1010)
      dec     -> hex : place-value sum in base 16 (15 \\times 16 + 15)
      hex     -> bin : each hex digit -> nibble   (1->0001, A->1010)
    """
    n = parse_value(value, frm)
    src = format_value(n, frm)
    if to == "dec":
        return r"$%s$" % _place_terms(src, _RADIX[frm])
    if to == "hex" and frm == "bin":
        return r"\texttt{%s}" % r"\,".join(_nibbles(src))
    if to == "hex" and frm == "dec":
        return r"$%s$" % _place_terms(format_value(n, "hex"), 16)
    if to == "bin" and frm == "hex":
        maps = [r"\texttt{%s}\!\to\!\texttt{%s}" % (ch, format(int(ch, 16), "04b"))
                for ch in src]
        return r"$%s$" % r",\ ".join(maps)
    return ""
