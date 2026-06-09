"""Worksheet 4 — hexadecimal, with Boolean-algebra & flowchart revision.

Number-base conversions (decimal / binary / hexadecimal, in every direction),
with one Boolean question and one flowchart trace mixed in as revision.

Each conversion is authored once: the values are given in the source base and
every answer is derived from the same integer. The revision questions are
ordinary boolgen / flowgen problem objects — bingen.build reuses those
generators' renderers, so nothing is duplicated.
"""

from bingen import CONVERT, BITMAP, IPV4
from boolgen import parse, DIAGRAM
from flowgen import Algorithm, read, assign, out, If, While, TRACE

TITLE = "Worksheet 4"

# Real-world capstone: a black-and-white picture is a grid of pixels, one byte
# per row. Authored as ASCII art ('#' = filled, '.' = blank); the hex bytes the
# student converts are derived from it, so they can't disagree with the picture.
heart = [
    ".##..##.",
    "########",
    "########",
    "########",
    ".######.",
    "..####..",
    "...##...",
    "........",
]

# Revision flowchart: one loop, two conditionals — the largest and smallest
# digit of n. (max starts at 0, min at 9, since every digit is between 0 and 9.)
digit_extremes = Algorithm("Largest and smallest digit", [
    read("n"),
    assign("max", "0"),
    assign("min", "9"),
    While("n > 0", [
        assign("d", "n % 10"),
        If("d > max", [assign("max", "d")]),
        If("d < min", [assign("min", "d")]),
        assign("n", "n // 10"),
    ]),
    out("max"),
    out("min"),
])

PROBLEMS = [
    # ---- base conversions, every direction ----
    CONVERT([26, 60, 175, 255], frm="dec", to="hex"),
    CONVERT(["1A", "2F", "B4", "FF"], frm="hex", to="dec"),

    # ---- revision: read the gate diagram (five gates) ----
    DIAGRAM(parse("((a | b) & c) | (a & ~b)")),

    CONVERT(["11010", "101111", "10110100", "1111"], frm="bin", to="hex"),
    CONVERT(["3C", "A7", "1E", "FF"], frm="hex", to="bin"),

    # ---- real-world: IP addresses are four bytes ----
    IPV4(["192.168.1.1", "10.0.0.255", "8.8.8.8"],
         spot=["192.168.0.1", "10.0.256.4", "172.16.0.255"],
         reflect="Fun fact: 8.8.8.8 is one of Google’s real public addresses."),

    # ---- real-world capstone: pixels are numbers ----
    BITMAP(heart, name="a heart",
           reflect="What picture appears? The whole image is just 8 bytes — "
                   "64 ones and zeros. Roughly how many bytes would a picture "
                   "twice as wide and twice as tall (16 × 16) need?"),

    # ---- revision: trace the flowchart (one loop, two conditionals) ----
    TRACE(digit_extremes, {"n": 5184}),
]
