"""A build-along worksheet activity.

This sheet is a *follow-along* guide, not a trace-and-predict set: each activity
is a small project the student builds in Scratch at the computer. So the unit
here is `BUILD` - a project with a goal, the new blocks it introduces, ordered
build steps, the finished script(s) to match, and a required "Your task" section.

"Your task" is not optional: after matching the finished script, the student must
work through its items in order, each one a small enhancement that builds on the
project (and on the previous item) - progressive enhancement. The finished script
is shown on BOTH the worksheet and the answer key (it is the thing the student is
building, so it is part of the instructions). The answer key adds the expected
result of each task; the worksheet leaves them for the student to do.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .script import Script


@dataclass
class Activity:
    title: str
    goal: str                                    # one line: what we build & why
    setup: str = ""                              # how to get ready (sprite/backdrop)
    new_blocks: list = field(default_factory=list)   # (block text, plain meaning)
    steps: list = field(default_factory=list)        # ordered build instructions (prose)
    scripts: list = field(default_factory=list)      # Script objects to display
    script_intro: str = ""                       # line above the rendered script(s)
    tasks: list = field(default_factory=list)    # (instruction, expected result) - result in key
    note: str = ""                               # an aside / tip
    stack: bool = False                          # force full-width, one-per-row scripts


def BUILD(title: str, *, goal: str, steps: list, scripts: list | Script,
          setup: str = "", new_blocks: list | None = None,
          script_intro: str = "When you are done, your code should look like this:",
          tasks: list | None = None, note: str = "", stack: bool = False) -> Activity:
    """One build project. `scripts` may be a single Script or a list of them.
    `tasks` is a list of (instruction, expected result) pairs - the required
    "Your task" work, done in order to extend the project. The instruction shows
    on the worksheet; the expected result shows only on the answer key. Set
    `stack=True` to render several scripts full-width, one per row, instead of
    two to a row - needed when a script carries a wide block (e.g. a long "your
    turn" gap hint) that would overrun a half-width column."""
    if isinstance(scripts, Script):
        scripts = [scripts]
    return Activity(title=title, goal=goal, setup=setup,
                    new_blocks=new_blocks or [], steps=steps, scripts=scripts,
                    script_intro=script_intro, tasks=tasks or [], note=note,
                    stack=stack)
