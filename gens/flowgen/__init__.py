"""flowgen — flowchart (simple-algorithm) practice-sheet generator for cs17.org.

Author each algorithm once; derive the flowchart, the pseudocode, and the trace
table from the same source so they can never disagree.
"""
from .algo import Algorithm, read, assign, out, If, While, run, pseudocode_text
from .bug import (missing, move_into_loop, swap_branches, wrong_assign,
                  wrong_cond, wrong_print)
from .problem import Problem, TRACE, DRAW, OUTPUTS, DEBUG
from .scratch import scratch_blocks

__all__ = ["Algorithm", "read", "assign", "out", "If", "While", "run",
           "pseudocode_text", "Problem", "TRACE", "DRAW", "OUTPUTS", "DEBUG",
           "wrong_cond", "wrong_assign", "wrong_print", "swap_branches",
           "missing", "move_into_loop", "scratch_blocks"]
