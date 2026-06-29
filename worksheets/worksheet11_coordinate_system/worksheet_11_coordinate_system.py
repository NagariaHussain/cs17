"""Coordinate-System & Turtle-Instructions Worksheet — prepare for Scratch.

This sheet is the on-paper primer for the Scratch stage. Scratch positions every
sprite on a coordinate grid centred on (0,0) — x across, y up — and moves them
with `go to x: y:`, `change x by`, `change y by`, `move` and `turn`. Here the
student practises that exact grid and those exact instructions with a turtle.

Like Worksheet 10, the sheet is mostly DRAW: a short Part A reads the grid to
build vocabulary, then every problem hands the student a target and asks them to
*write the instructions* (instruct the turtle), not just trace given ones. Each
turtle program is authored once; the answer key's drawing, endpoint and heading
are all derived from that one source, so they can never disagree.

It ramps deliberately:

  Part A  read the grid          — coordinates, the origin, the four quadrants
  Part B  write absolute moves   — go to (x, y)
  Part C  write relative moves   — change x by / change y by
  Part D  write turtle drawings  — move / turn (a heading), with pen up/down

ending with a dino capstone that ties the whole grid back to the Chrome Dino
game the students are about to build in Scratch.
"""

from gens.turtlegen import (
    TurtleProgram, fd, lt, rt, goto, changex, changey, penup, pendown,
    READGRID, TRACE, DRAW,
)

TITLE = "Worksheet 11: Coordinates and the Turtle"

# ---- Part A: read the grid (coordinates, origin, quadrants) -------------------

# A1. read off four points, one in each quadrant.
read_quadrants = READGRID(
    points=[("A", 4, 2), ("B", -3, 3), ("C", -4, -2), ("D", 2, -4)],
    extent=6,
    reveal="Notice the signs: top-right is $(+,+)$, top-left $(-,+)$, "
           "bottom-left $(-,-)$, bottom-right $(+,-)$. Scratch points work the "
           "same way.")

# A2. plot four given points onto a blank grid.
plot_points = READGRID(
    plot=[("P", 2, 4), ("Q", -3, 2), ("R", -2, -4), ("S", 3, -1)],
    extent=6)

# A3. read off points that sit ON the axes (where one coordinate is 0).
read_axes = READGRID(
    points=[("E", 0, 3), ("F", -4, 0), ("G", 0, -2), ("H", 5, 0)],
    extent=6,
    note="These points sit on a line, not in a corner — so one of their two "
         "numbers is 0.",
    reveal="A point on the up–down line has x = 0; a point on the across line "
           "has y = 0. The origin $(0,0)$ is on both.")

# ---- Part B: write absolute moves — go to (x, y) -----------------------------

# B1. trace a square whose corners are read straight off the grid.
square_origin = TurtleProgram("Square from the origin", [
    goto(4, 0), goto(4, 4), goto(0, 4), goto(0, 0),
])

# B2. an L plus a separate stroke — needs a pen-up jump between them.
two_strokes = TurtleProgram("Two separate strokes", [
    goto(0, 3), goto(3, 3),
    penup(), goto(-3, -2), pendown(),
    goto(-3, 2),
])

# B3. a treasure-map triangle: visit three marked spots in order.
triangle = TurtleProgram("Treasure triangle", [
    goto(-3, -2), goto(3, -2), goto(0, 3), goto(-3, -2),
], start=(-3, -2))

# ---- Part C: write relative moves — change x by / change y by ----------------

# C1. reach a point from the origin using one change-x and one change-y.
reach_point = TurtleProgram("Reach the point", [
    changex(5), changey(3),
], heading=90)

# C2. reach a point that needs NEGATIVE changes (going left and down).
reach_negative = TurtleProgram("Reach the point (going back)", [
    changex(-5), changey(-4),
], start=(2, 5))

# C3. draw a staircase with the pen down, using only change-x / change-y.
staircase = TurtleProgram("Staircase", [
    changex(2), changey(2), changex(2), changey(2), changex(2),
], start=(-4, -3))

# ---- Part D: write turtle drawings — move / turn (a heading) -----------------

# D1. a square drawn with move + turn, starting facing up.
turtle_square = TurtleProgram("Square with move and turn", [
    fd(4), rt(90), fd(4), rt(90), fd(4), rt(90), fd(4),
])

# D2. a 5-wide, 3-tall rectangle with move + turn.
turtle_rectangle = TurtleProgram("Rectangle with move and turn", [
    fd(3), rt(90), fd(5), rt(90), fd(3), rt(90), fd(5),
])

# D3. an upward staircase using move + turn (turning left then right).
turtle_steps = TurtleProgram("Steps with move and turn", [
    fd(2), rt(90), fd(2), lt(90), fd(2), rt(90), fd(2), lt(90), fd(2),
], start=(-4, -3))

# ---- Capstone: the dino's jump (ties the grid back to the Scratch game) ------

dino_jump = TurtleProgram("The dino's jump", [
    changey(5), changey(-5),
], start=(-6, -4))


PROBLEMS = [
    # ---- Part A: read the grid ----------------------------------------------
    read_quadrants,
    plot_points,
    read_axes,

    # ---- Part B: write absolute moves ---------------------------------------
    DRAW(square_origin,
         target="The turtle starts at the origin with its pen down. Write "
                "\\cmd{go to} instructions to draw this square, visiting each "
                "corner in order.",
         show="shape", label_vertices=True, extent=6),

    DRAW(two_strokes,
         target="Draw these two separate strokes. The turtle's pen must be "
                "lifted while it jumps from the end of the first stroke to the "
                "start of the second.",
         show="shape", label_vertices=True, extent=6,
         note="Use \\cmd{pen up} before the jump and \\cmd{pen down} after it, "
              "or the jump will leave an unwanted line.",
         reveal="A dashed line in the answer key means the pen was up — the "
                "turtle moved but drew nothing."),

    DRAW(triangle,
         target="Starting at the bottom-left spot, write \\cmd{go to} "
                "instructions to visit the three treasure spots and return to "
                "the start, drawing the triangle.",
         show="shape", label_vertices=True, extent=6),

    # ---- Part C: write relative moves ---------------------------------------
    DRAW(reach_point,
         target="The turtle is at the origin. Write \\cmd{change x by} and "
                "\\cmd{change y by} instructions to move it to the target.",
         show="point", extent=6,
         note="\\cmd{change} adds to where the turtle already is. How far across "
              "is the target, and how far up?"),

    DRAW(reach_negative,
         target="The turtle starts at $(2,5)$. Write \\cmd{change} instructions "
                "to move it to the target. You will need negative numbers.",
         show="point", extent=6,
         note="To move left, change x by a negative number; to move down, "
              "change y by a negative number."),

    DRAW(staircase,
         target="The turtle starts at $(-4,-3)$ with its pen down. Write "
                "\\cmd{change x by} / \\cmd{change y by} instructions to draw "
                "this staircase.",
         show="shape", extent=6),

    # ---- Part D: write turtle drawings (move / turn) ------------------------
    DRAW(turtle_square,
         target="This time use \\cmd{move} and \\cmd{turn} instead of "
                "\\cmd{go to}. The turtle starts at the origin facing up. Write "
                "the instructions to draw this square.",
         show="shape", extent=6,
         note="\\cmd{move} goes forward in whatever direction the turtle is "
              "facing; \\cmd{turn} changes that direction without drawing."),

    DRAW(turtle_rectangle,
         target="Using \\cmd{move} and \\cmd{turn}, draw this rectangle "
                "(5 across, 3 up). The turtle starts at the origin facing up.",
         show="shape", extent=6),

    DRAW(turtle_steps,
         target="Using \\cmd{move} and \\cmd{turn}, draw these steps. The "
                "turtle starts at $(-4,-3)$ facing up. Watch which way it must "
                "turn at each corner.",
         show="shape", extent=6,
         note="Turning left then right then left keeps the turtle climbing in "
              "steps rather than closing a box."),

    # ---- Capstone: the dino's jump ------------------------------------------
    DRAW(dino_jump,
         target="Here is a mini Scratch stage (1 square = 20 steps). The Dino "
                "rests on the floor; a cactus slides in from the right. Write "
                "the \\cmd{change y by} instructions for the Dino's jump: go up "
                "5, then come back down 5 to land on the floor.",
         show="dino", extent=8,
         note="The Dino never moves across — it only changes y. The cactus "
              "passes underneath using \\cmd{change x by} a negative number.",
         reveal="In the real game the floor is at y = $-80$ and the cactus "
                "spawns at x = $240$. The Dino stays at one x and only "
                "\\cmd{change y by} to jump, while the cactus slides left with "
                "\\cmd{change x by}. You just wrote the heart of the game.")
]
