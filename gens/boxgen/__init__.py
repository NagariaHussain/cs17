"""boxgen — the anchor-point worksheet generator (Worksheet 16).

A box on the coordinate grid is one anchor point plus a width and a height. This
package models that box (`box.Box`, the single source of truth), poses five kinds
of problem over it (`problem`: NAME / PLACE / COMPUTE / DECIDE / GROUND), draws it
inline on the grid shared with turtlegen (`grid`, `..gridframe`), and renders the
capstone's Scratch grounded-check by reusing scratchgen's block renderer
(`latex`). It teaches why a sprite's $(x, y)$ is its centre, and why the on-the-
ground test must use the feet (the bottom edge), not the centre.
"""

from .box import Box
from .problem import COMPUTE, DECIDE, GROUND, NAME, PLACE, Problem

__all__ = ["Box", "Problem", "NAME", "PLACE", "COMPUTE", "DECIDE", "GROUND"]
