"""termgen - terminal & shell practice sheets.

Author one archive (`gens.termgen.tree`) and one list of plain-English actions
(`gens.termgen.task`); the generator produces the worksheet PDF, the answer key
PDF, and the `.zip` the student extracts to do the work - all from that single
source, so the tree printed on the sheet and the numbers in the key always match
the folder on the student's machine.

    from gens.termgen import D, F, IMG, PART, TASK, PATHS, ERRORS, PREDICT

    ARCHIVE = D("cs17-archive", [...])
    PARTS   = [PART("Where am I?", tasks=[TASK("Print where you are.", cmd="pwd")])]
"""

from .tree import (
    D, F, IMG, Dir, File, Image,
    ascii_tree, check_case_collisions, find, grep_lines, listing, make_zip,
    match, materialise, ngrep, nlines, text, walk,
)
from .task import (
    PART, TASK, PATHS, ERRORS, PREDICT, BOX,
    Part, Task, PathTable, ErrorTable, Predict, Box,
)

__all__ = [
    "D", "F", "IMG", "Dir", "File", "Image",
    "ascii_tree", "check_case_collisions", "find", "grep_lines", "listing",
    "make_zip", "match", "materialise", "ngrep", "nlines", "text", "walk",
    "PART", "TASK", "PATHS", "ERRORS", "PREDICT", "BOX",
    "Part", "Task", "PathTable", "ErrorTable", "Predict", "Box",
]
