"""Render a `Script` as scratch3 LaTeX — the picture the student matches.

A second view of the same source the prose steps describe, so the blocks shown
and the build instructions can never drift apart. The mapping is direct: each
block's `category` picks the scratch3 colour macro, and the already-formatted
`label` (ovals + menus baked in by script.py) goes straight inside it. C-blocks
recurse into their body.

scratch3 facts that shape this (all handled in the worksheet preamble, see
latex.py): the `forever` cap has no bottom nub and keeps its loop arrow, which
the package's public macros don't expose, so it is drawn with the internal
`\\blockforever` we define; `repeat (n)` is the built-in `\\blockrepeat{n}{body}`.
"""

from __future__ import annotations

from .script import Block, CBlock, Script, Gap, _esc

# category -> the scratch3 colour macro for an ordinary stack block
_CAT = {
    "event":     r"\blockinit",     # an event hat (when ... clicked / received)
    "broadcast": r"\blockevent",    # an event-coloured *stack* block (broadcast)
    "move":      r"\blockmove",
    "look":      r"\blocklook",
    "sound":     r"\blocksound",
    "control":   r"\blockcontrol",
    "sensing":   r"\blocksensing",
    "data":      r"\blockvariable",
}


def _indent(lines: list[str]) -> list[str]:
    return ["  " + ln for ln in lines]


def _cond(label, answer: bool) -> str:
    """Resolve an if / repeat-until header. A plain (already-formatted) label
    passes through; a `Gap` label becomes the real boolean on the key, or a grey
    "your turn" hexagon (\\boolgap) on the worksheet, so the `if` shell still
    shows with only its test left blank."""
    if isinstance(label, Gap):
        if answer:
            return "".join(str(x) for x in label.real)
        return r"\boolgap{%s}" % _esc(label.hint)
    return label


def _emit(blocks: list, answer: bool = False) -> list[str]:
    lines: list[str] = []
    for b in blocks:
        if isinstance(b, Gap):
            # On the answer key a gap becomes the real block(s); on the worksheet
            # it is a grey "your turn" placeholder carrying the plain-words hint.
            if answer:
                lines += _emit(b.real, answer)
            else:
                lines.append(r"\blockgap{%s}" % _esc(b.hint))
        elif isinstance(b, CBlock):
            if b.kind == "forever":
                lines.append(r"\blockforever{")
                lines += _indent(_emit(b.body, answer))
                lines.append("}")
            elif b.kind == "repeat":
                # \blockrepeat takes the count as its first argument, body second
                count = b.label[len("repeat "):]  # the \ovalnum{...} script.py built
                lines.append(r"\blockrepeat{%s}{" % count)
                lines += _indent(_emit(b.body, answer))
                lines.append("}")
            elif b.kind == "repeatuntil":
                # \blockrepeatuntil is defined in the preamble (latex.py) the same
                # way \blockforever is — the package has no public repeat-until.
                lines.append(r"\blockrepeatuntil{%s}{" % _cond(b.label, answer))
                lines += _indent(_emit(b.body, answer))
                lines.append("}")
            elif b.kind == "if":
                # scratch3 draws the header band verbatim and adds no "if"/"then"
                # of its own (only "else", via the else-word KV), so the wording
                # must be supplied here or the block shows a bare hexagon.
                lines.append(r"\blockif{if %s then}{" % _cond(b.label, answer))
                lines += _indent(_emit(b.body, answer))
                lines.append("}")
            elif b.kind == "ifelse":
                # "if <cond> then" here; the package draws the "else" bar itself.
                lines.append(r"\blockifelse{if %s then}{" % _cond(b.label, answer))
                lines += _indent(_emit(b.body, answer))
                lines.append("}{")
                lines += _indent(_emit(b.body2, answer))
                lines.append("}")
            else:
                raise AssertionError(b.kind)
        elif isinstance(b, Block):
            lines.append(r"%s{%s}" % (_CAT[b.category], b.label))
        else:
            raise AssertionError(b)
    return lines


def render_script(s: Script, scale: float = 1.0, answer: bool = False) -> str:
    """The full `scratch` environment for one script (hat + body). With
    `answer=True`, any `Gap` in the body is rendered as its real block(s);
    otherwise a gap is drawn as a grey "your turn" placeholder."""
    lines = [r"\begin{scratch}[%.2f]" % scale,
             r"%s{%s}" % (_CAT[s.hat.category], s.hat.label)]
    lines += _emit(s.body, answer)
    lines.append(r"\end{scratch}")
    return "\n".join(lines)


def render_blocks(blocks: list, scale: float = 1.0, answer: bool = False) -> str:
    """A `scratch` environment for a loose stack of blocks with no hat — e.g. a
    single `if` shown on its own, as boxgen does for the grounded-check."""
    lines = [r"\begin{scratch}[%.2f]" % scale]
    lines += _emit(blocks, answer)
    lines.append(r"\end{scratch}")
    return "\n".join(lines)
