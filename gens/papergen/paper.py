"""The exam-paper model: a paper is sections, a section is questions, a question
is parts, and every part carries its marks.

This is the piece the worksheet generators have no use for. A worksheet is a
flat list of problems with no weighting; a paper has a marks budget that must
add up, an exam header (duration, maximum marks, instructions), and per-section
scenarios. Marks are never restated by hand: a question totals its parts and a
paper totals its sections, and `Paper.check()` asserts the declared maximum
matches what the parts actually add up to.

Prose fields are author-trusted LaTeX (they carry \\blk{...}, \\emph{}, \\%
on purpose), exactly as scratchgen treats its step and note text.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Cell:
    """One spreadsheet cell in a shown table. `blank` marks a column the student
    has to fill with a formula — drawn as an empty shaded box."""
    value: str = ""
    blank: bool = False


@dataclass(frozen=True)
class SheetTable:
    """A table shown as a real spreadsheet grid: lettered columns across the top,
    numbered rows down the side, so the cell references in the question text
    ("in cell I18") point at something the student can actually see.

    `columns` is a list of (letter, heading) pairs; `rows` is a list of row-value
    lists, each as long as `columns`; `blank_from` names the first column letter
    that is left empty for the student.
    """
    sheet: str
    columns: tuple
    rows: tuple
    blank_from: str = ""
    note: str = ""
    new_page: bool = False      # start this table at the top of a fresh page, so a
                                # long grid is never split from its sheet heading

    @property
    def letters(self) -> tuple:
        return tuple(letter for letter, _ in self.columns)

    @property
    def headings(self) -> tuple:
        return tuple(head for _, head in self.columns)

    def is_blank(self, letter: str) -> bool:
        if not self.blank_from:
            return False
        return self.letters.index(letter) >= self.letters.index(self.blank_from)


@dataclass(frozen=True)
class Part:
    """One lettered part of a question — the unit that carries marks.

    `items` are the (i)/(ii)/(iii) sub-instructions. `answer` and `answer_items`
    are the key's prose; `scripts` are scratchgen `Script`s shown on the key only
    (a Scratch part's model solution).
    """
    label: str
    marks: int
    title: str = ""             # a short heading after the label, so the heading
                                # line reads as a phrase rather than a bare "(a)"
                                # with the marks stranded at the far margin
    text: str = ""
    items: tuple = ()
    note: str = ""
    given: tuple = ()           # scratchgen Scripts the student is GIVEN — shown on
                                # both documents (a trace question needs the script
                                # on the paper, not just on the key)
    answer: str = ""
    answer_items: tuple = ()
    scripts: tuple = ()         # model-solution Scripts — answer key only
    answer_note: str = ""


@dataclass(frozen=True)
class Question:
    number: int
    title: str = ""
    intro: str = ""
    given: tuple = ()           # Scripts every part refers to — shown once under
                                # the intro, above the parts, on both documents
    parts: tuple = ()

    @property
    def marks(self) -> int:
        return sum(p.marks for p in self.parts)


@dataclass(frozen=True)
class Section:
    """A section: its own scenario, its own data tables, its own questions."""
    name: str
    title: str = ""
    scenario: str = ""
    tables: tuple = ()
    questions: tuple = ()
    outro: str = ""
    new_page: bool = False      # start this section at the top of a fresh page

    @property
    def marks(self) -> int:
        return sum(q.marks for q in self.questions)


@dataclass(frozen=True)
class Paper:
    title: str
    duration: str = ""
    max_marks: int | None = None
    instructions: tuple = ()
    sections: tuple = ()
    footer_note: str = ""

    @property
    def marks(self) -> int:
        return sum(s.marks for s in self.sections)

    def check(self):
        """A declared maximum that disagrees with the parts is an authoring bug,
        not something to discover after the paper is printed."""
        if self.max_marks is not None and self.max_marks != self.marks:
            raise AssertionError(
                f"paper declares {self.max_marks} marks but the parts add up to "
                f"{self.marks} — " +
                ", ".join(f"{s.name}: {s.marks}" for s in self.sections))
        return self
