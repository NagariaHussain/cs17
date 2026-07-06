"""Anchor-Point Worksheet — where a box sits on the grid (Scratch prep).

Worksheet 11 taught the grid with *points*. But a Scratch sprite is not a point,
it is a box, and Scratch pins that box to the grid by one chosen point: its
centre. This sheet makes that idea concrete with a plain rectangle. The student
learns that the same box has many addresses (centre, four corners, four edges),
how to move between them with `centre ± (w/2, h/2)`, and why the on-the-ground
test in the Dino game must use the feet (the bottom edge), not the centre.

Like Worksheets 11 and 12, every problem derives from one source (a `Box`), so
the drawing, the blanks and the answer key can never disagree. It ramps:

  Part A  NAME     read the parts of a drawn box
  Part B  PLACE    given an anchor point + w + h, draw the box
  Part C  COMPUTE  no picture: work out a part from the centre (centre ± w/2, h/2)
  Part D  DECIDE   is the box above / on / below the floor, and why
  Part E  GROUND   write the real Scratch grounded-check block (three of them)
"""

from gens.boxgen import Box, NAME, PLACE, COMPUTE, DECIDE, GROUND
from gens.scratchgen.script import sety, changey, broadcast

TITLE = "Worksheet 16: Anchor Points"

PROBLEMS = [
    # ---- Part A: read the parts of a drawn box ------------------------------
    NAME(Box("center", 2, 1, 4, 2), parts=["BL", "BR", "TL", "TR"], extent=6),

    NAME(Box("center", -3, -1, 6, 4), parts=["TL", "BR", "bottom", "top"],
         extent=7,
         note="Two of these are corners (two numbers each). Two are whole "
              "edges, so they need only one number."),

    NAME(Box("center", 1, -2, 2, 6), parts=["BL", "TR", "left", "right"],
         extent=6,
         note="A tall, thin box. The left edge and the right edge each sit on "
              "one up-down line, so each has a single x."),

    # ---- Part B: place the box ----------------------------------------------
    PLACE(Box("center", 1, 1, 4, 2),
          target="Draw a box that is 4 wide and 2 tall, with its \\textbf{centre} "
                 "at $(1,1)$. Mark the four corners.",
          extent=6),

    PLACE(Box("BL", -4, -3, 5, 3),
          target="This time you are given a \\emph{corner}, not the centre. Draw "
                 "a box 5 wide and 3 tall whose \\textbf{bottom-left corner} is "
                 "at $(-4,-3)$.",
          extent=6,
          note="Same kind of numbers as before, but the box lands in a "
               "different place. From the bottom-left corner the box goes to "
               "the right and up.",
          reveal="Notice the centre is not at $(-4,-3)$ here. Choosing a "
                 "different anchor point moves the whole box."),

    PLACE(Box("TR", 4, 4, 6, 4),
          target="Draw a box 6 wide and 4 tall whose \\textbf{top-right corner} "
                 "is at $(4,4)$. From the top-right corner the box goes to the "
                 "left and down.",
          extent=6),

    # ---- Part C: compute a part from the centre (no picture) ----------------
    COMPUTE(Box("center", 0, 0, 4, 2), parts=["TR", "BL", "bottom"],
            note="Half the width is $4 \\div 2 = 2$; half the height is "
                 "$2 \\div 2 = 1$."),

    COMPUTE(Box("center", 5, 3, 2, 4), parts=["BR", "TL", "top"]),

    COMPUTE(Box("center", -2, 4, 8, 6), parts=["BL", "BR", "TL", "TR", "bottom"],
            note="A big box. Half the width is 4, half the height is 3."),

    # ---- Part D: is the box above / on / below the floor? -------------------
    DECIDE(Box("center", 0, 1, 4, 2), floor=-3,
           target="The brown line is the floor. Is the box above it, resting on "
                  "it, or below it? Look at the feet (the bottom edge), not the "
                  "centre.",
           extent=6),

    DECIDE(Box("center", 0, 0, 4, 4), floor=-2,
           target="Is this box above the floor, on it, or below it? Work out "
                  "where the feet are first.",
           extent=6),

    DECIDE(Box("center", -1, 1, 4, 6), floor=0,
           target="And this tall box? Its centre looks like it is well above "
                  "the floor. Check the feet before you decide.",
           extent=6,
           note="The centre can be above the floor while the feet are already "
                "below it. That is exactly the trap the Dino game sets."),

    # ---- Part E: write the Scratch grounded-check block (capstone x3) --------
    GROUND(Box("center", 0, 0, 4, 5), floor=-80, half=25,
           action=[sety(-55)], grounded=True,
           target="Now the real Scratch stage. The floor is at $y=-80$. The Dino "
                  "is 50 tall, so \\cmd{y position} minus 25 is its feet. Write "
                  "the \\cmd{if} that is true when the Dino has landed on the "
                  "floor. When it lands, set its centre to $-55$ so the feet "
                  "rest on $-80$.",
           why="The feet are \\cmd{y position} $-\\,25$. They reach the floor "
               "when that value drops to $-80$, so the test is "
               "\\cmd{(y position) $-$ 25 \\textless{} $-80$}. Setting the "
               "centre to $-55$ puts the feet exactly on $-80$ ($-55-25=-80$)."),

    GROUND(Box("center", 0, 3, 4, 5), floor=-80, half=25,
           action=[changey(-5)], grounded=False, negate=True,
           target="While the Dino is jumping it is \\emph{above} the floor. "
                  "Write the \\cmd{if} that is true while the Dino is still in "
                  "the air (its feet have \\emph{not} reached the floor yet). "
                  "While it is, pull it down by 5.",
           note="\"Still in the air\" is the opposite of \"landed\". You can "
                "wrap the landed test in \\cmd{not}.",
           why="Landed is \\cmd{(y position) $-$ 25 \\textless{} $-80$}. Still "
               "in the air is the opposite, so wrap it in \\cmd{not}. Pulling "
               "down by 5 each time is gravity."),

    GROUND(Box("center", 0, 2, 4, 4), floor=-50, half=20,
           action=[broadcast("game over")], grounded=False,
           target="A different check. The top of the cactus is at $y=-50$, and "
                  "this Dino is 40 tall (so subtract 20 for its feet). Write the "
                  "\\cmd{if} that is true when the Dino's feet drop below the top "
                  "of the cactus. If they do, broadcast \\cmd{game over}.",
           note="Same shape as before, but a different line ($-50$, not $-80$) "
                "and a different height (subtract 20, not 25).",
           why="The feet are \\cmd{y position} $-\\,20$. Below the cactus top "
               "means less than $-50$: \\cmd{(y position) $-$ 20 \\textless{} "
               "$-50$}. You wrote the same pattern three times with different "
               "numbers. That is the whole grounded-check idea."),
]
