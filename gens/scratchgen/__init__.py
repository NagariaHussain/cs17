"""scratchgen — build-along Scratch-project worksheet generator for cs17.org.

Author each finished Scratch script once (script.py, the single source); render
it to scratch3 blocks (render.py) so the picture the student matches is exactly
the script the prose build steps describe. The worksheet is a follow-along guide
to building small projects in Scratch — basic blocks, movement, and events.
"""

from .script import (
    Block, CBlock, Gap, Expr, Script, script, gap,
    when_flag, when_key, when_clicked, when_receive, when_clone,
    move, turn_right, turn_left, goto_xy, glide, point,
    point_towards, goto, glide_to,
    changex, changey, setx, sety, bounce, set_rotation_style,
    x_position, y_position, direction,
    say, say_for, think, show, hide, next_costume, switch_costume,
    switch_backdrop, change_size, set_size,
    play_sound, play_until,
    wait, forever, repeat, wait_until, stop_all, if_, ifelse, repeat_until,
    create_clone, delete_clone,
    broadcast, broadcast_wait,
    define, call_block,
    set_var, change_var, show_var, hide_var, var,
    ask, answer, mouse_x, mouse_y, timer, distance_to,
    touching, touching_color, key_pressed, mouse_down,
    pick_random, join, add, sub, mul, div, gt, lt, eq, and_, or_, not_,
)
from .render import render_script
from .problem import Activity, BUILD

__all__ = [
    "Block", "CBlock", "Gap", "Expr", "Script", "script", "gap",
    "when_flag", "when_key", "when_clicked", "when_receive", "when_clone",
    "move", "turn_right", "turn_left", "goto_xy", "glide", "point",
    "point_towards", "goto", "glide_to",
    "changex", "changey", "setx", "sety", "bounce", "set_rotation_style",
    "x_position", "y_position", "direction",
    "say", "say_for", "think", "show", "hide", "next_costume", "switch_costume",
    "switch_backdrop", "change_size", "set_size",
    "play_sound", "play_until",
    "wait", "forever", "repeat", "wait_until", "stop_all",
    "if_", "ifelse", "repeat_until",
    "create_clone", "delete_clone",
    "broadcast", "broadcast_wait",
    "define", "call_block",
    "set_var", "change_var", "show_var", "hide_var", "var",
    "ask", "answer", "mouse_x", "mouse_y", "timer", "distance_to",
    "touching", "touching_color", "key_pressed", "mouse_down",
    "pick_random", "join", "add", "sub", "mul", "div",
    "gt", "lt", "eq", "and_", "or_", "not_",
    "render_script", "Activity", "BUILD",
]
