"""examgen — exam question papers (title block + parts + questions -> PDF).

A paper module authors PARTS; each question is built by one of the
constructors below. Flowchart questions wrap flowgen problems and Boolean
questions wrap boolgen expressions, so the exam reuses the same single-source
machinery as the worksheets. No answer key is produced.
"""
from .question import (PART, Part, Question, BOOL, CALC, DEBUG, DRAW, GATEMCQ,
                       MCQ, Q, SHEET, SHORT, TBD, TRACE)

__all__ = ["PART", "Part", "Question", "Q", "SHORT", "MCQ", "GATEMCQ",
           "SHEET", "CALC", "TBD", "BOOL", "TRACE", "DRAW", "DEBUG"]
