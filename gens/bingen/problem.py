"""A binary / hexadecimal worksheet problem.

  TODECIMAL  given binary numbers           -> write each in decimal
  TOBINARY   given decimal numbers          -> write each in binary
  CONVERT    given numbers in one base      -> write each in another base
  DECODE     given ASCII codes in binary    -> decode the message (ASCII table)
  BITMAP     given a picture's bytes in hex -> convert + shade -> the image appears
  IPV4       given IP addresses             -> convert each byte to 8-bit binary
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .convert import BASE_NAME, parse_value

KINDS = ("todecimal", "tobinary", "convert", "decode", "bitmap", "ipv4")


@dataclass
class Problem:
    kind: str
    binaries: list[str] = field(default_factory=list)  # todecimal: the numbers
    decimals: list[int] = field(default_factory=list)  # tobinary: the numbers
    values: list = field(default_factory=list)          # convert: the numbers
    frm: str = ""                                       # convert: source base
    to: str = ""                                        # convert: target base
    message: str = ""                                   # decode: the plaintext
    rows: list = field(default_factory=list)            # bitmap: ASCII-art rows
    name: str = ""                                       # bitmap: what the picture is
    reflect: str = ""                                    # bitmap/ipv4: open-ended closing prompt
    spot: list = field(default_factory=list)            # ipv4: "which is not valid?" candidates
    width: int = 8                                      # decode: bit-width of each code;
                                                        # tobinary: 0 = natural width (no padding)
    note: str = ""        # in-question hint (e.g. notation not yet taught)
    description: str = ""  # plain-English scenario shown before the task

    def __post_init__(self):
        assert self.kind in KINDS, f"unknown kind {self.kind!r}"
        if self.kind == "todecimal":
            for b in self.binaries:
                assert set(b) <= {"0", "1"} and b, f"not a binary number: {b!r}"
        if self.kind == "tobinary":
            for n in self.decimals:
                assert isinstance(n, int) and n >= 0, f"not a non-negative int: {n!r}"
        if self.kind == "convert":
            assert self.frm in BASE_NAME and self.to in BASE_NAME, "bad base"
            assert self.frm != self.to, "source and target base are the same"
            for v in self.values:
                parse_value(v, self.frm)  # raises if not a valid `frm` number
        if self.kind == "bitmap":
            assert self.rows, "empty bitmap"
            w = len(self.rows[0])
            assert all(len(r) == w for r in self.rows), "bitmap rows differ in width"
        if self.kind == "ipv4":
            for a in self.values:  # the ones to convert must be valid
                octs = a.split(".")
                assert len(octs) == 4 and all(
                    o.isdigit() and int(o) <= 255 for o in octs), \
                    f"not a valid IPv4 address: {a!r}"


def TODECIMAL(*binaries: str, note: str = "", description: str = "") -> Problem:
    """Convert each binary number (a string of 0/1, e.g. "1011") to decimal."""
    return Problem("todecimal", binaries=list(binaries), note=note,
                   description=description)


def TOBINARY(*decimals: int, width: int = 0, note: str = "",
             description: str = "") -> Problem:
    """Convert each decimal number to binary. `width` pads to a fixed number of
    bits (e.g. 8); the default 0 uses each number's natural width."""
    return Problem("tobinary", decimals=list(decimals), width=width, note=note,
                   description=description)


def CONVERT(values: list, *, frm: str, to: str, note: str = "",
            description: str = "") -> Problem:
    """Convert each value from base `frm` to base `to` (each "bin"/"dec"/"hex").
    Values are strings (or ints for decimal) written in the `frm` base."""
    return Problem("convert", values=list(values), frm=frm, to=to, note=note,
                   description=description)


def BITMAP(rows: list, *, name: str = "", reflect: str = "",
           description: str = "") -> Problem:
    """A pixel picture authored as ASCII art (rows of '#'/'.', same width). The
    student is given each row as a hex byte, converts to binary, and shades the
    1-bits to reveal the image. `name` is the reveal shown on the answer key."""
    return Problem("bitmap", rows=list(rows), name=name, reflect=reflect,
                   description=description)


def IPV4(addresses: list, *, spot: list = None, reflect: str = "",
         description: str = "") -> Problem:
    """Convert each dotted IPv4 address to binary (each of its four bytes -> 8
    bits). `spot` is an optional list of candidate addresses for a "which of
    these could not be a real address?" part (one has a byte > 255)."""
    return Problem("ipv4", values=list(addresses), spot=list(spot or []),
                   reflect=reflect, description=description)


def DECODE(message: str, *, width: int = 8, note: str = "",
           description: str = "") -> Problem:
    """Decode a message: each character is given as its ASCII code in `width`-bit
    binary; the student converts to decimal and looks the character up."""
    return Problem("decode", message=message, width=width, note=note,
                   description=description)
