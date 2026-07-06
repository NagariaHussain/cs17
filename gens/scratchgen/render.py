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

from .script import Block, CBlock, Script

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


def _emit(blocks: list) -> list[str]:
    lines: list[str] = []
    for b in blocks:
        if isinstance(b, CBlock):
            if b.kind == "forever":
                lines.append(r"\blockforever{")
                lines += _indent(_emit(b.body))
                lines.append("}")
            elif b.kind == "repeat":
                # \blockrepeat takes the count as its first argument, body second
                count = b.label[len("repeat "):]  # the \ovalnum{...} script.py built
                lines.append(r"\blockrepeat{%s}{" % count)
                lines += _indent(_emit(b.body))
                lines.append("}")
            elif b.kind == "repeatuntil":
                # \blockrepeatuntil is defined in the preamble (latex.py) the same
                # way \blockforever is — the package has no public repeat-until.
                lines.append(r"\blockrepeatuntil{%s}{" % b.label)
                lines += _indent(_emit(b.body))
                lines.append("}")
            elif b.kind == "if":
                lines.append(r"\blockif{%s}{" % b.label)
                lines += _indent(_emit(b.body))
                lines.append("}")
            elif b.kind == "ifelse":
                lines.append(r"\blockifelse{%s}{" % b.label)
                lines += _indent(_emit(b.body))
                lines.append("}{")
                lines += _indent(_emit(b.body2))
                lines.append("}")
            else:
                raise AssertionError(b.kind)
        elif isinstance(b, Block):
            lines.append(r"%s{%s}" % (_CAT[b.category], b.label))
        else:
            raise AssertionError(b)
    return lines


def render_script(s: Script, scale: float = 1.0) -> str:
    """The full `scratch` environment for one script (hat + body)."""
    lines = [r"\begin{scratch}[%.2f]" % scale,
             r"%s{%s}" % (_CAT[s.hat.category], s.hat.label)]
    lines += _emit(s.body)
    lines.append(r"\end{scratch}")
    return "\n".join(lines)


def render_blocks(blocks: list, scale: float = 1.0) -> str:
    """A `scratch` environment for a loose stack of blocks with no hat — e.g. a
    single `if` shown on its own, as boxgen does for the grounded-check."""
    lines = [r"\begin{scratch}[%.2f]" % scale]
    lines += _emit(blocks)
    lines.append(r"\end{scratch}")
    return "\n".join(lines)
