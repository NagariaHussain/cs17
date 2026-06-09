"""bingen — binary-numbers practice-sheet generator for cs17.org.

Author each problem once; derive every representation from the same source so
they can never disagree:
  - a conversion problem is one binary string  -> decimal is computed from it
  - a decode problem is one plaintext message  -> the ASCII codes are derived

Two problem kinds: TODECIMAL (binary -> decimal) and DECODE (ASCII codes -> text).
"""
from .binary import (ascii_label, encode, expansion, from_binary, place_values,
                     to_binary)
from .problem import BITMAP, CONVERT, DECODE, IPV4, TOBINARY, TODECIMAL, Problem

__all__ = ["Problem", "TODECIMAL", "TOBINARY", "CONVERT", "DECODE", "BITMAP",
           "IPV4", "ascii_label", "encode", "expansion", "from_binary",
           "place_values", "to_binary"]
