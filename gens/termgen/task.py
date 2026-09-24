"""The units a terminal worksheet is made of.

This sheet is neither a trace-and-predict set nor a follow-along build: it is a
**hands-on drill**. The student sits at a real terminal, in a real folder, and
turns a plain-English action into a command. So the unit is `TASK`: the action
in English on the worksheet, the model command plus its expected output on the
answer key only. That split is the whole point - the lesson plan's teacher note
says not to hand out a one-to-one command list.

Three tasks are tables rather than list items, because writing a path (or an
error message) by hand is the exercise:

- `PATHS`  - "you are here, you want to get there: write the relative path, then
             the absolute one". Absolute-vs-relative is the module's main mental
             model, so it gets its own drill.
- `ERRORS` - a broken command per row; the student runs it, copies the error
             back, and says why. Errors are information, not failure.
- `PREDICT`- write down what you think the command prints, *then* run it.

One unit is not a drill but a blank: `BOX` reserves a framed, ruled-free area
for something the student copies off the screen by hand (the archive map). It
prints empty on the worksheet and filled on the answer key, so the teacher can
check the copy against the real thing.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Task:
    text: str                  # the action, in plain English (author LaTeX)
    cmd: str = ""              # model command(s) - answer key only
    expect: str = ""           # what it prints / what changes - answer key only
    write: int = 0             # ruled lines for the student's answer
    hint: str = ""             # shown on the worksheet (a nudge, not the answer)
    given: str = ""            # command(s) printed on BOTH documents (see TASK)


@dataclass
class PathTable:
    rows: list                 # (you are here, you want, relative, absolute)
    caption: str = ""
    absolute: bool = True      # False -> drop the absolute-path column


@dataclass
class ErrorTable:
    rows: list                 # (broken command, error message, why it failed)
    caption: str = ""


@dataclass
class Predict:
    rows: list                 # (command, what it prints)
    caption: str = ""


@dataclass
class Box:
    prompt: str                # author LaTeX, printed above the frame
    height: float = 7.0        # frame height in cm, worksheet only
    answer: str = ""           # what belongs in it - answer key only


@dataclass
class Part:
    title: str
    lesson: str = ""                              # "Lesson 1", for the teacher
    intro: str = ""                               # author LaTeX
    recap: list = field(default_factory=list)     # (command, what it does)
    tasks: list = field(default_factory=list)
    note: str = ""                                # a tip / safety aside
    bonus: bool = False                           # flagged "not covered yet"


def TASK(text: str, *, cmd: str = "", expect: str = "", write: int = 0,
         hint: str = "", given: str = "") -> Task:
    """One action. `text` is what the student reads. `cmd` and `expect` print on
    the answer key only. `write` is how many ruled lines to leave for a written
    answer (0 when the task is pure doing and leaves its result on disk).

    `given` prints the commands on the worksheet as well. Use it only for a
    command the sheet has not taught and does not test - the archive has to be
    unzipped before lesson 1 exists, and a student cannot be asked to work out
    `unzip` from first principles. Everything the sheet does teach stays in
    `cmd`, on the answer key only."""
    return Task(text=text, cmd=cmd, expect=expect, write=write, hint=hint,
                given=given)


def BOX(prompt: str, *, height: float = 7.0, answer: str = "") -> Box:
    """A framed blank for a hand copy. `prompt` says what to write in it,
    `height` is centimetres of empty frame on the printed sheet, and `answer`
    is the text that belongs there, printed on the answer key in place of the
    blank. Use it where ruled lines are wrong because the shape of the answer
    matters - an indented tree, a drawing - and a run of \ansline would flatten
    it."""
    return Box(prompt=prompt, height=height, answer=answer)


def PATHS(rows: list, *, caption: str = "", absolute: bool = True) -> PathTable:
    """Path drill. Each row is (standing in, want to reach, relative, absolute);
    pass `absolute=False` for a relative-only table and give 3-tuples."""
    return PathTable(rows=[tuple(r) for r in rows], caption=caption,
                     absolute=absolute)


def ERRORS(rows: list, *, caption: str = "") -> ErrorTable:
    """Run-it-and-read-it drill: (broken command, the error, why)."""
    return ErrorTable(rows=[tuple(r) for r in rows], caption=caption)


def PREDICT(rows: list, *, caption: str = "") -> Predict:
    """Predict-before-Enter drill: (command, what it prints)."""
    return Predict(rows=[tuple(r) for r in rows], caption=caption)


def PART(title: str, *, tasks: list, lesson: str = "", intro: str = "",
         recap: list | None = None, note: str = "", bonus: bool = False) -> Part:
    """One part of the sheet. `recap` is the (command, meaning) table printed at
    the top - the only cheat sheet the student gets, and only for the commands
    that part needs. `bonus=True` marks a part as material not taught yet."""
    return Part(title=title, lesson=lesson, intro=intro, recap=recap or [],
                tasks=tasks, note=note, bonus=bonus)
