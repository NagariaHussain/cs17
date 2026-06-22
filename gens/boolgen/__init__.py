"""boolgen — Boolean-algebra practice-sheet generator for cs17.org.

One expression per problem -> gate diagram + formula + truth table, all
derived from the same source so they can never disagree.
"""
from .expr import (V, NOT, AND, OR, NAND, NOR, XOR, XNOR, parse,
                   variables, evaluate, truth_table)
from .problem import Problem, DIAGRAM, CIRCUIT, TRUTHTABLE, FROMTABLE

__all__ = ["V", "NOT", "AND", "OR", "NAND", "NOR", "XOR", "XNOR", "parse",
           "variables", "evaluate", "truth_table",
           "Problem", "DIAGRAM", "CIRCUIT", "TRUTHTABLE", "FROMTABLE"]
