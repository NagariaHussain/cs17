"""flowgen — flowchart (simple-algorithm) practice-sheet generator for cs17.org.

Author each algorithm once; derive the flowchart, the pseudocode, and the trace
table from the same source so they can never disagree.
"""
from .algo import Algorithm, read, assign, out, If, While, run, pseudocode_text
from .problem import Problem, TRACE, DRAW, OUTPUTS
from .scratch import scratch_blocks

__all__ = ["Algorithm", "read", "assign", "out", "If", "While", "run",
           "pseudocode_text", "Problem", "TRACE", "DRAW", "OUTPUTS",
           "scratch_blocks"]
