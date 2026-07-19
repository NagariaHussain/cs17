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


class Expr(str):
    """A finished scratch3 fragment — a coloured reporter oval or boolean hexagon
    (e.g. the `score` reporter or `touching edge?`). It is a plain string of LaTeX,
    tagged so input slots know to drop it in as-is instead of wrapping it in a white
    `\\ovalnum`. Authors build these with the reporter/boolean helpers below and nest
    them inside other blocks: ``set_var("x", pick_random(-200, 200))``."""


def _arg(v) -> str:
    """An input slot: an already-built reporter/boolean passes through untouched; a
    plain number or short string becomes a white `\\ovalnum` input."""
    return str(v) if isinstance(v, Expr) else _oval(v)


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


@dataclass
class Gap:
    """A "your turn" hole in the script: on the worksheet it draws a grey
    placeholder block carrying `hint` (what the student must add, in plain words);
    on the answer key it renders `real` (the block(s) that belong there) instead.
    A gap stands in for one or more stack blocks, or a whole C-block, at a single
    slot in a stack - the missing piece the student drags in themselves."""
    hint: str           # plain-words goal, e.g. "add 1 to the score"
    real: list          # the Block/CBlock(s) shown filled in on the answer key


# ---- event hats (every script starts with one) ------------------------------

def when_flag() -> Block:
    return Block("event", r"when \greenflag\ clicked")


def when_key(key: str) -> Block:
    """`key` is a key name as Scratch lists it: 'space', 'right arrow', 'a', ..."""
    return Block("event", r"when %s key pressed" % _menu(key))


def when_clicked() -> Block:
    return Block("event", r"when this sprite clicked")


def when_receive(msg) -> Block:
    """when I receive [message] — runs when any sprite broadcasts `msg`."""
    return Block("event", r"when I receive %s" % _menu(msg))


def when_clone() -> Block:
    """when I start as a clone — a hat that runs on each new clone the moment it
    is born. It is a Control block in Scratch, but rendered with the event hat
    macro (the scratch3 package ships only one hat shape); category 'event' keeps
    it hat-shaped rather than a stack block."""
    return Block("event", r"when I start as a clone")


# ---- motion ------------------------------------------------------------------

def move(n) -> Block:
    return Block("move", r"move %s steps" % _arg(n))


def turn_right(deg) -> Block:
    return Block("move", r"turn \turnright\ %s degrees" % _arg(deg))


def turn_left(deg) -> Block:
    return Block("move", r"turn \turnleft\ %s degrees" % _arg(deg))


def goto_xy(x, y) -> Block:
    return Block("move", r"go to x: %s y: %s" % (_arg(x), _arg(y)))


def glide(secs, x, y) -> Block:
    return Block("move", r"glide %s secs to x: %s y: %s"
                 % (_arg(secs), _arg(x), _arg(y)))


def point(deg) -> Block:
    return Block("move", r"point in direction %s" % _arg(deg))


def point_towards(target="mouse-pointer") -> Block:
    """point towards [mouse-pointer] / another sprite — a dropdown target."""
    return Block("move", r"point towards %s" % _menu(target))


def goto(target="random position") -> Block:
    """go to [random position] / [mouse-pointer] / a sprite — a dropdown target.
    (For a fixed spot use `goto_xy`.)"""
    return Block("move", r"go to %s" % _menu(target))


def glide_to(secs, target="random position") -> Block:
    """glide [secs] secs to [mouse-pointer] / [random position] / a sprite."""
    return Block("move", r"glide %s secs to %s" % (_arg(secs), _menu(target)))


def changex(n) -> Block:
    return Block("move", r"change x by %s" % _arg(n))


def changey(n) -> Block:
    return Block("move", r"change y by %s" % _arg(n))


def setx(n) -> Block:
    return Block("move", r"set x to %s" % _arg(n))


def sety(n) -> Block:
    return Block("move", r"set y to %s" % _arg(n))


def bounce() -> Block:
    return Block("move", r"if on edge, bounce")


def set_rotation_style(style="left-right") -> Block:
    return Block("move", r"set rotation style %s" % _menu(style))


# motion reporters (blue ovals) — the sprite's own position / heading
def x_position() -> Expr:
    return Expr(r"\ovalmove{x position}")


def y_position() -> Expr:
    return Expr(r"\ovalmove{y position}")


def direction() -> Expr:
    return Expr(r"\ovalmove{direction}")


# ---- looks -------------------------------------------------------------------

def say(text) -> Block:
    return Block("look", r"say %s" % _arg(text))


def say_for(text, secs=2) -> Block:
    return Block("look", r"say %s for %s seconds" % (_arg(text), _arg(secs)))


def think(text) -> Block:
    return Block("look", r"think %s" % _arg(text))


def show() -> Block:
    return Block("look", r"show")


def hide() -> Block:
    return Block("look", r"hide")


def next_costume() -> Block:
    return Block("look", r"next costume")


def switch_costume(name) -> Block:
    return Block("look", r"switch costume to %s" % _menu(name))


def switch_backdrop(name) -> Block:
    return Block("look", r"switch backdrop to %s" % _menu(name))


def change_size(n) -> Block:
    return Block("look", r"change size by %s" % _arg(n))


def set_size(n) -> Block:
    return Block("look", r"set size to %s \%%" % _arg(n))


# ---- sound -------------------------------------------------------------------

def play_sound(name) -> Block:
    return Block("sound", r"start sound %s" % _menu(name))


def play_until(name) -> Block:
    return Block("sound", r"play sound %s until done" % _menu(name))


# ---- control -----------------------------------------------------------------

def wait(secs=1) -> Block:
    return Block("control", r"wait %s seconds" % _arg(secs))


def forever(*body) -> CBlock:
    return CBlock("forever", r"forever", list(body))


def repeat(n, *body) -> CBlock:
    return CBlock("repeat", r"repeat %s" % _arg(n), list(body))


def wait_until(cond) -> Block:
    """wait until <cond> — pause until a boolean hexagon becomes true."""
    return Block("control", r"wait until %s" % cond)


def stop_all() -> Block:
    return Block("control", r"stop %s" % _menu("all"))


def create_clone(target="myself") -> Block:
    """create clone of [myself] — make a live copy that runs its own
    `when I start as a clone` script."""
    return Block("control", r"create clone of %s" % _menu(target))


def delete_clone() -> Block:
    """delete this clone — remove this clone so they do not pile up."""
    return Block("control", r"delete this clone")


def _condlabel(cond):
    """The header slot of an if / repeat-until. A `Gap` cond stays a Gap so
    render.py can resolve it per document (a grey "your turn" hexagon on the
    worksheet, the real boolean on the key); anything else is stringified now, as
    before. This is what lets the `if` shell show while its test is left blank."""
    return cond if isinstance(cond, Gap) else str(cond)


def if_(cond, *body) -> CBlock:
    """if <cond> then [body] — a C-block whose body runs once when `cond` is true.
    `cond` is a boolean hexagon (see `touching`, `gt`, ...), or a `gap(...)` to
    leave the test blank for the student while still drawing the `if` shell."""
    return CBlock("if", _condlabel(cond), list(body))


def ifelse(cond, then, orelse) -> CBlock:
    """if <cond> then [then] else [orelse] — `then` and `orelse` are block lists."""
    return CBlock("ifelse", _condlabel(cond), list(then), list(orelse))


def repeat_until(cond, *body) -> CBlock:
    """repeat until <cond> [body] — loop until the boolean hexagon `cond` is true."""
    return CBlock("repeatuntil", _condlabel(cond), list(body))


# ---- events: broadcast (a stack block, not a hat) ----------------------------

def broadcast(msg) -> Block:
    return Block("broadcast", r"broadcast %s" % _menu(msg))


def broadcast_wait(msg) -> Block:
    return Block("broadcast", r"broadcast %s and wait" % _menu(msg))


# ---- data: variables ---------------------------------------------------------

def set_var(name, value) -> Block:
    return Block("data", r"set %s to %s" % (_menu(name), _arg(value)))


def change_var(name, by) -> Block:
    return Block("data", r"change %s by %s" % (_menu(name), _arg(by)))


def show_var(name) -> Block:
    return Block("data", r"show variable %s" % _menu(name))


def hide_var(name) -> Block:
    return Block("data", r"hide variable %s" % _menu(name))


def var(name) -> Expr:
    """The variable's reporter oval — drop it into any input: `say(var("score"))`."""
    return Expr(r"\ovalvariable{%s}" % _esc(name))


# ---- sensing: reporters (ovals) and predicates (hexagons) --------------------

def ask(prompt) -> Block:
    return Block("sensing", r"ask %s and wait" % _arg(prompt))


def answer() -> Expr:
    return Expr(r"\ovalsensing{answer}")


def mouse_x() -> Expr:
    return Expr(r"\ovalsensing{mouse x}")


def mouse_y() -> Expr:
    return Expr(r"\ovalsensing{mouse y}")


def timer() -> Expr:
    return Expr(r"\ovalsensing{timer}")


def distance_to(target="mouse-pointer") -> Expr:
    return Expr(r"\ovalsensing{distance to %s}" % _menu(target))


def touching(target="mouse-pointer") -> Expr:
    return Expr(r"\boolsensing{touching %s?}" % _menu(target))


def touching_color(color) -> Expr:
    return Expr(r"\boolsensing{touching color %s?}" % _menu(color))


def key_pressed(key="space") -> Expr:
    return Expr(r"\boolsensing{key %s pressed?}" % _menu(key))


def mouse_down() -> Expr:
    return Expr(r"\boolsensing{mouse down?}")


# ---- operators: reporters (ovals) and predicates (hexagons) ------------------
# Operators are never stack blocks — only green ovals/hexagons nested in inputs.

def pick_random(a, b) -> Expr:
    return Expr(r"\ovaloperator{pick random %s to %s}" % (_arg(a), _arg(b)))


def join(a, b) -> Expr:
    return Expr(r"\ovaloperator{join %s %s}" % (_arg(a), _arg(b)))


def add(a, b) -> Expr:
    return Expr(r"\ovaloperator{%s + %s}" % (_arg(a), _arg(b)))


def sub(a, b) -> Expr:
    return Expr(r"\ovaloperator{%s $-$ %s}" % (_arg(a), _arg(b)))


def mul(a, b) -> Expr:
    return Expr(r"\ovaloperator{%s $\times$ %s}" % (_arg(a), _arg(b)))


def div(a, b) -> Expr:
    return Expr(r"\ovaloperator{%s / %s}" % (_arg(a), _arg(b)))


def gt(a, b) -> Expr:
    return Expr(r"\booloperator{%s \textgreater\ %s}" % (_arg(a), _arg(b)))


def lt(a, b) -> Expr:
    return Expr(r"\booloperator{%s \textless\ %s}" % (_arg(a), _arg(b)))


def eq(a, b) -> Expr:
    return Expr(r"\booloperator{%s = %s}" % (_arg(a), _arg(b)))


def and_(a, b) -> Expr:
    return Expr(r"\booloperator{%s and %s}" % (a, b))


def or_(a, b) -> Expr:
    return Expr(r"\booloperator{%s or %s}" % (a, b))


def not_(a) -> Expr:
    return Expr(r"\booloperator{not %s}" % a)


# ---- a "your turn" gap the student fills in ----------------------------------

def gap(hint: str, *real) -> Gap:
    """A hole in the script for the student to fill. `hint` is the plain-words
    goal shown on the worksheet placeholder; `real` is the block(s) that belong
    there, shown only on the answer key: `gap("add 1 to the score",
    change_var("score", 1))`."""
    return Gap(hint, list(real))


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
