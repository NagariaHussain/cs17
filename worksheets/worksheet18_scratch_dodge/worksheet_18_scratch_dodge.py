"""Scratch F - Rock Dodge: a second capstone, more gaps to fill yourself.

Scratch E built a catch-and-score game. Scratch F is a dodge-and-survive game,
built the same follow-along way: most blocks are given to drag together, and a
few grey "your turn" gaps are left for you. The star gap is the rock's reset,
which uses the \\blk{y position} idea from Worksheet 16 (Anchor Points): a
sprite's y position is its centre, and we test when it has fallen off the bottom.

  Project 1  move left and right    ground movement with the arrow keys
  Project 2  make the rock fall     a falling rock that returns to the top
  Project 3  crash and score        touch a rock -> game over, survive -> score

By the end the student has a complete survival game, and has written the falling
loop, the off-screen test, and the crash check that drive it.
"""

from gens.scratchgen import (
    BUILD, script, gap,
    when_flag,
    goto_xy, changex, changey, y_position,
    say_for, set_size,
    forever, if_, wait, stop_all,
    set_var, change_var, var,
    touching, key_pressed, lt, pick_random,
)
from gens.scratchgen.stage import sketch

TITLE = "Scratch F"

PALETTE = ["Motion", "Looks", "Sound", "Events", "Control",
           "Sensing", "Operators", "Variables"]

LEAD = (
    r"\textbf{Welcome to Scratch F - Rock Dodge.}\quad One more game, built the "
    r"same way as Coin Dash: most of it is given, and the grey \blk{? your turn} "
    r"blocks are gaps you fill in. This time you dodge falling rocks and survive "
    r"as long as you can. The trickiest gap uses an idea from Worksheet 16: a "
    r"sprite's \blk{y position} is the height of its \emph{centre}, so when that "
    r"number drops below the bottom of the stage, the rock has fallen off. Open "
    r"\texttt{scratch.mit.edu}, click \emph{Create}, and let us build it."
    + sketch(
        markers=[
            (0, -150, "Player", "orange"),
            (90, 120, "Rock", "brown!70"),
        ],
        motions=[(0, -150, "leftright"), (90, 120, "down")],
        readouts=[("score", "0")],
        ground=-168,
        caption="Slide the Player left and right along the ground to dodge the "
                "falling Rock. Score counts the seconds you survive.",
    ))


# ---- Project 1: move left and right ------------------------------------------

p1 = BUILD(
    "Move left and right",
    goal="Put the player on the ground and let it slide left and right with the "
         "arrow keys. It does not jump. It just dodges along the bottom.",
    setup="Rename the cat sprite to \\textbf{Player}. You will keep it near the "
          "bottom of the stage, where it can dodge the falling rocks.",
    steps=[
        "On the \\textbf{Player}, start with \\blk{when green flag clicked}, then "
        "\\blk{go to x: 0 y: -150} (down on the ground) and \\blk{set size to "
        "(60) \\%}.",
        "Add a \\blk{forever} loop. Inside it, the right arrow is given in full: "
        "\\blk{if <key [right arrow] pressed?>} then \\blk{change x by (10)}.",
        "Below it is a second \\blk{if} shell for the left arrow. Both blanks are "
        "\\blk{? your turn}: fill the grey hexagon with the left-arrow test, and "
        "the grey block with the move. Copy the pattern from the right arrow, but "
        "the other way.",
        "Green flag, and slide left and right along the ground.",
    ],
    script_intro="The Player's movement loop. The right arrow is done; fill the "
                 "two grey gaps in the left-arrow \\blk{if}:",
    scripts=script(
        when_flag(),
        goto_xy(0, -150),
        set_size(60),
        forever(
            if_(key_pressed("right arrow"), changex(10)),
            if_(gap("is the left arrow pressed?", key_pressed("left arrow")),
                gap("move the player to the left", changex(-10))),
        ),
        caption="Player: dodge left and right",
    ),
    note="The player only ever changes x, so its height never changes. It stays "
         "locked to the ground line at y: -150 all game.",
    tasks=[
        ("Change both \\blk{10} and \\blk{-10} to move faster or slower. Pick a "
         "speed that feels fair against the rocks.",
         "A faster player dodges more easily; a slower one is a harder game."),
        ("Keep the player on screen: the stage edge is x: 240, so it cannot run "
         "off. Try \\blk{go to x: -150 y: -150} at the start to begin on the "
         "left.", "The player begins each game in the same spot."),
    ],
)


# ---- Project 2: make the rock fall -------------------------------------------

p2 = BUILD(
    "Make the rock fall",
    goal="Add a rock that starts at the top at a random spot, falls straight "
         "down, and jumps back to the top once it drops off the bottom. That is "
         "one rock falling again and again, forever.",
    setup="Add a \\textbf{Rock} sprite (click \\emph{Choose a Sprite}, pick a "
          "rock, an apple, or a ball, and rename it \\textbf{Rock}). Make it "
          "small so it fits the stage.",
    new_blocks=[
        ("y position", "A blue Motion reporter: the height of the sprite's centre. It is a plus number near the top and a minus number near the bottom."),
        ("if <(y position) $<$ (-170)>", "True when the rock's centre has dropped below the bottom edge of the stage."),
    ],
    steps=[
        "On the \\textbf{Rock}, start with \\blk{when green flag clicked}, then "
        "\\blk{set size to (50) \\%}.",
        "Add \\blk{go to x: (pick random (-220) to (220)) y: (170)}. That drops "
        "the rock in at a random column, up at the top.",
        "Add a \\blk{forever} loop. Its first block is given: \\blk{change y by "
        "(-6)}, which makes the rock fall.",
        "The next block is an \\blk{if} shell, with two \\blk{? your turn} gaps. "
        "The grey hexagon is the test: has the rock fallen off the bottom? Think "
        "about the \\blk{y position} block from Worksheet 16. The grey block "
        "inside is the action: send the rock back to the top at a new random "
        "column.",
        "Green flag. The rock falls, and the moment it leaves the bottom it "
        "reappears up top somewhere new.",
    ],
    script_intro="The Rock's falling loop. Fill the \\blk{if}: its test (the grey "
                 "hexagon) and its action (the grey block):",
    scripts=script(
        when_flag(),
        set_size(50),
        goto_xy(pick_random(-220, 220), 170),
        forever(
            changey(-6),
            if_(gap("has the rock dropped below the bottom?",
                    lt(y_position(), -170)),
                gap("send the rock to the top at a random x",
                    goto_xy(pick_random(-220, 220), 170))),
        ),
        caption="Rock: fall and reset",
    ),
    note="The bottom edge is y: -180. Testing \\blk{y position \\textless\\ -170} "
         "resets the rock just as its centre slips past the bottom, so it never "
         "gets stuck off screen.",
    tasks=[
        ("Make the rock fall faster: change \\blk{change y by (-6)} to a bigger "
         "drop like \\blk{-9}.",
         "A faster rock is harder to dodge."),
        ("Add a second rock: right-click the Rock and choose \\emph{duplicate}. "
         "The copy runs the same script, so now two rocks fall at once.",
         "Two rocks fall in random columns, doubling the danger."),
    ],
)


# ---- Project 3: crash and score ----------------------------------------------

p3 = BUILD(
    "Mini project: crash and score",
    goal="Make it a real game. A \\blk{score} counts how many seconds you "
         "survive, and touching a rock ends the game. The longer you last, the "
         "higher you score.",
    setup="Make a variable \\textbf{score} \\emph{For all sprites}. Both new "
          "scripts below go on the \\textbf{Player}.",
    new_blocks=[
        ("if <touching [Rock]?>", "True when the player is touching a rock. That is the crash."),
    ],
    steps=[
        "On the \\textbf{Player}, add a scoring script: \\blk{when green flag "
        "clicked}, then \\blk{set [score] to (0)}, then a \\blk{forever} loop "
        "whose first block is \\blk{wait (1) seconds}.",
        "The next block is a \\blk{? your turn}: add one to the score on every "
        "tick, so the score counts the seconds you survive.",
        "Add a second script for the crash: \\blk{when green flag clicked} then "
        "a \\blk{forever} loop.",
        "Inside it is an \\blk{if} shell that ends the game. Its inside blocks "
        "(\\blk{say (Crash!)} and \\blk{stop [all]}) are given. The \\blk{? your "
        "turn} is the grey hexagon: fill in the test for touching a rock.",
        "Green flag, and dodge. Your score climbs each second until a rock "
        "catches you.",
    ],
    script_intro="The scoring loop, then the crash loop. Fill the grey stack "
                 "block, and the grey hexagon in the \\blk{if}:",
    stack=True,
    scripts=[
        script(
            when_flag(),
            set_var("score", 0),
            forever(
                wait(1),
                gap("add 1 to the score",
                    change_var("score", 1)),
            ),
            caption="Player: one point per second",
        ),
        script(
            when_flag(),
            forever(
                if_(gap("is the player touching a rock?", touching("Rock")),
                    say_for("Crash!", 2),
                    stop_all()),
            ),
            caption="Player: game over on a hit",
        ),
    ],
    note="The score loop waits a second between points, but the crash loop has "
         "no wait, so it checks for a hit as fast as it can. That keeps the game "
         "fair: you never touch a rock without it counting.",
    tasks=[
        ("Show the result: change \\blk{say (Crash!) for (2) seconds} to include "
         "the score, like \\blk{say (join (Score: ) (score))}.",
         "The game ends by telling the player their final score."),
        ("Give three lives instead of instant death. Make a variable "
         "\\blk{lives}, \\blk{set [lives] to (3)} at the start, and in the crash "
         "loop \\blk{change [lives] by (-1)}.",
         "The player can take three hits before the game ends."),
        ("End only when the lives run out: wrap the crash in \\blk{if <(lives) "
         "= (0)>} then \\blk{stop [all]}.",
         "The game stops on the third hit, not the first."),
    ],
)


ACTIVITIES = [p1, p2, p3]
