"""scratchgen — build-along Scratch-project worksheet generator for cs17.org.

Author each finished Scratch script once (script.py, the single source); render
it to scratch3 blocks (render.py) so the picture the student matches is exactly
the script the prose build steps describe. The worksheet is a follow-along guide
to building small projects in Scratch — basic blocks, movement, and events.
"""

from .script import (
    Block, CBlock, Script, script,
    when_flag, when_key, when_clicked,
    move, turn_right, turn_left, goto_xy, glide, point,
    changex, changey, setx, sety, bounce, set_rotation_style,
    say, say_for, think, show, hide, next_costume, switch_costume,
    change_size, set_size,
    play_sound, play_until,
    wait, forever, repeat,
)
from .render import render_script
from .problem import Activity, BUILD

__all__ = [
    "Block", "CBlock", "Script", "script",
    "when_flag", "when_key", "when_clicked",
    "move", "turn_right", "turn_left", "goto_xy", "glide", "point",
    "changex", "changey", "setx", "sety", "bounce", "set_rotation_style",
    "say", "say_for", "think", "show", "hide", "next_costume", "switch_costume",
    "change_size", "set_size",
    "play_sound", "play_until",
    "wait", "forever", "repeat",
    "render_script", "Activity", "BUILD",
]
