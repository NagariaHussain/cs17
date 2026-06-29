"""The Scratch-script model — the single source of truth for a build project.

Unlike flowgen (which models an *algorithm* and derives a flowchart / trace from
it), scratchgen models a *Scratch script directly*: a hat block with a stack of
blocks under it, exactly as it appears on the Scratch code canvas. A worksheet
authors the finished script once here, and the build-along sheet renders it with
the scratch3 package (-> render.py) so the picture the student matches block by
block is the very script described in the prose steps.

A `Script` is one hat (`when ... clicked / pressed`) plus a body of blocks. A
project usually has several scripts (one per arrow key, one for the green flag,
one for the sprite click), so a worksheet activity carries a list of them.

Each constructor returns a `Block` (a single stack block) or a `CBlock` (a
C-shaped wrapper: forever / repeat / if) whose `label` is already the formatted
scratch3 text — the white ovals (`\\ovalnum`) and dropdown menus (`\\selectmenu`)
are baked in here so render.py only has to pick the category colour and recurse.
The block vocabulary is the beginner subset: motion, looks, sound, simple
control, and the three event hats. That is deliberately the "basic blocks,
movement, events" surface and no more.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ---- text escaping (block labels are typeset, not verbatim) ------------------

def _esc(s) -> str:
    s = str(s)
    for a, b in [("\\", r"\textbackslash{}"), ("&", r"\&"), ("%", r"\%"),
                 ("#", r"\#"), ("_", r"\_"), ("{", r"\{"), ("}", r"\}"),
                 ("~", r"\textasciitilde{}"), ("^", r"\textasciicircum{}"),
                 ("$", r"\$")]:
        s = s.replace(a, b)
    return s


def _num(v) -> str:
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return _esc(v)


def _oval(v) -> str:
    """A white input oval — what a number or short text slot looks like."""
    return r"\ovalnum{%s}" % _num(v)


def _menu(v) -> str:
    """A dropdown slot (key name, costume name, sound name, ...)."""
    return r"\selectmenu{%s}" % _esc(v)


# ---- block types -------------------------------------------------------------

@dataclass
class Block:
    """One ordinary stack block. `category` selects the colour (-> render.py);
    `label` is the finished scratch3 text with its ovals/menus already in place."""
    category: str       # 'event' | 'move' | 'look' | 'sound' | 'control' | 'sensing'
    label: str


@dataclass
class CBlock:
    """A C-shaped wrapper that holds a body: forever / repeat / if / if-else."""
    kind: str           # 'forever' | 'repeat' | 'if' | 'ifelse'
    label: str          # header text (already formatted), e.g. r"repeat \ovalnum{10}"
    body: list
    body2: list = field(default_factory=list)   # the else branch, for 'ifelse'


# ---- event hats (every script starts with one) ------------------------------

def when_flag() -> Block:
    return Block("event", r"when \greenflag\ clicked")


def when_key(key: str) -> Block:
    """`key` is a key name as Scratch lists it: 'space', 'right arrow', 'a', ..."""
    return Block("event", r"when %s key pressed" % _menu(key))


def when_clicked() -> Block:
    return Block("event", r"when this sprite clicked")


# ---- motion ------------------------------------------------------------------

def move(n) -> Block:
    return Block("move", r"move %s steps" % _oval(n))


def turn_right(deg) -> Block:
    return Block("move", r"turn \turnright\ %s degrees" % _oval(deg))


def turn_left(deg) -> Block:
    return Block("move", r"turn \turnleft\ %s degrees" % _oval(deg))


def goto_xy(x, y) -> Block:
    return Block("move", r"go to x: %s y: %s" % (_oval(x), _oval(y)))


def glide(secs, x, y) -> Block:
    return Block("move", r"glide %s secs to x: %s y: %s"
                 % (_oval(secs), _oval(x), _oval(y)))


def point(deg) -> Block:
    return Block("move", r"point in direction %s" % _oval(deg))


def changex(n) -> Block:
    return Block("move", r"change x by %s" % _oval(n))


def changey(n) -> Block:
    return Block("move", r"change y by %s" % _oval(n))


def setx(n) -> Block:
    return Block("move", r"set x to %s" % _oval(n))


def sety(n) -> Block:
    return Block("move", r"set y to %s" % _oval(n))


def bounce() -> Block:
    return Block("move", r"if on edge, bounce")


def set_rotation_style(style="left-right") -> Block:
    return Block("move", r"set rotation style %s" % _menu(style))


# ---- looks -------------------------------------------------------------------

def say(text) -> Block:
    return Block("look", r"say %s" % _oval(text))


def say_for(text, secs=2) -> Block:
    return Block("look", r"say %s for %s seconds" % (_oval(text), _oval(secs)))


def think(text) -> Block:
    return Block("look", r"think %s" % _oval(text))


def show() -> Block:
    return Block("look", r"show")


def hide() -> Block:
    return Block("look", r"hide")


def next_costume() -> Block:
    return Block("look", r"next costume")


def switch_costume(name) -> Block:
    return Block("look", r"switch costume to %s" % _menu(name))


def change_size(n) -> Block:
    return Block("look", r"change size by %s" % _oval(n))


def set_size(n) -> Block:
    return Block("look", r"set size to %s \%%" % _oval(n))


# ---- sound -------------------------------------------------------------------

def play_sound(name) -> Block:
    return Block("sound", r"start sound %s" % _menu(name))


def play_until(name) -> Block:
    return Block("sound", r"play sound %s until done" % _menu(name))


# ---- control -----------------------------------------------------------------

def wait(secs=1) -> Block:
    return Block("control", r"wait %s seconds" % _oval(secs))


def forever(*body) -> CBlock:
    return CBlock("forever", r"forever", list(body))


def repeat(n, *body) -> CBlock:
    return CBlock("repeat", r"repeat %s" % _oval(n), list(body))


# ---- the script container ----------------------------------------------------

@dataclass
class Script:
    """One hat plus the blocks stacked beneath it. `caption` is an optional short
    label shown under the rendered script (e.g. "Move right")."""
    hat: Block
    body: list = field(default_factory=list)
    caption: str = ""


def script(hat: Block, *body, caption: str = "") -> Script:
    """Author a script as `script(when_flag(), move(10), say("Hi"))`."""
    assert hat.category == "event", "a script must start with an event hat block"
    return Script(hat, list(body), caption=caption)
