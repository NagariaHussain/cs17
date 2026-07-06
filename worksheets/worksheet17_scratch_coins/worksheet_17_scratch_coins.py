"""Scratch E - Coin Dash: build one game, filling the gaps yourself.

Scratch A to D taught the blocks. Scratch E is a capstone: one small game,
Coin Dash, built in three follow-along stages. Most of each script is given for
you to drag together, but a few blocks are left as grey "your turn" gaps that
you must add yourself. Every gap is a block you have already met - a loop body,
a comparison, a change to a variable.

  Project 1  steer the player, drop a coin   arrow-key movement + a random coin
  Project 2  grab it, score up               touch the coin -> score, coin re-spawns
  Project 3  beat the clock                   a countdown that ends the game

By the end the student has a complete score-and-timer game, and has written the
loop, conditional, and variable pieces that make it work.
"""

from gens.scratchgen import (
    BUILD, script, gap,
    when_flag,
    goto_xy, changex, changey,
    say, say_for, set_size,
    forever, if_, wait, stop_all,
    set_var, change_var, var,
    touching, key_pressed, eq, pick_random,
)
from gens.scratchgen.stage import sketch

TITLE = "Scratch E"

PALETTE = ["Motion", "Looks", "Sound", "Events", "Control",
           "Sensing", "Operators", "Variables"]

LEAD = (
    r"\textbf{Welcome to Scratch E - Coin Dash.}\quad You have all the blocks "
    r"now. This sheet builds \emph{one} game in three stages: a player you steer "
    r"to catch coins before the clock runs out. Most of each script is given, "
    r"ready to drag together. But watch for the grey \blk{? your turn} blocks: "
    r"each one is a gap \emph{you} must fill with the right block. The finished "
    r"picture shows what to build. The grey block tells you what is missing, in "
    r"plain words. Every missing block is one you have used before. Open "
    r"\texttt{scratch.mit.edu}, click \emph{Create}, and let us play."
    + sketch(
        markers=[
            (0, 0, "Player", "orange"),
            (150, 95, "Coin", "yellow!85!orange"),
        ],
        motions=[(0, 0, "both")],
        readouts=[("score", "0"), ("time", "30")],
        caption="Steer the Player to catch the Coin before time runs out. "
                "Score and time show top-left.",
    ))


# ---- Project 1: steer the player and drop a coin -----------------------------

p1 = BUILD(
    "Steer the player, drop a coin",
    goal="Steer the cat with the arrow keys, the smooth way: one forever loop "
         "that reads all four keys. Then add a Coin sprite that starts at a "
         "random spot on the stage.",
    setup="Rename the cat sprite to \\textbf{Player}. Then add a coin: click "
          "\\emph{Choose a Sprite}, pick a ball or a doughnut, and rename it "
          "\\textbf{Coin}.",
    steps=[
        "On the \\textbf{Player}, start with \\blk{when green flag clicked}, then "
        "\\blk{go to x: 0 y: 0} and \\blk{set size to (60) \\%}.",
        "Add a \\blk{forever} loop. Inside it, add four choices, one per arrow "
        "key: \\blk{if <key [right arrow] pressed?>} then \\blk{change x by (5)}; "
        "\\textbf{left arrow} with \\blk{change x by (-5)}; \\textbf{up arrow} "
        "with \\blk{change y by (5)}; \\textbf{down arrow} with \\blk{change y "
        "by (-5)}.",
        "Click the green flag and steer with the arrow keys.",
        "Now click the \\textbf{Coin}. Give it \\blk{when green flag clicked}. "
        "The last block is your first \\blk{? your turn}: put the coin at a "
        "random spot so it is not in the same place every game.",
    ],
    script_intro="The Player's steering script, then the Coin's start. The grey "
                 "block is yours to fill:",
    stack=True,
    scripts=[
        script(
            when_flag(),
            goto_xy(0, 0),
            set_size(60),
            forever(
                if_(key_pressed("right arrow"), changex(5)),
                if_(key_pressed("left arrow"), changex(-5)),
                if_(key_pressed("up arrow"), changey(5)),
                if_(key_pressed("down arrow"), changey(-5)),
            ),
            caption="Player: steer with the arrows",
        ),
        script(
            when_flag(),
            gap("put the coin at a random spot on the stage",
                goto_xy(pick_random(-200, 200), pick_random(-140, 140))),
            caption="Coin: start somewhere random",
        ),
    ],
    note="The stage runs from x: -240 to 240 and y: -180 to 180. Staying inside "
         "about -200 to 200 and -140 to 140 keeps the coin fully on screen.",
    tasks=[
        ("Change \\blk{set size to (60) \\%} so the player is the size you like. "
         "Try 40 for a tiny, nippy cat.",
         "A smaller player is easier to squeeze through the stage."),
        ("Slow the player down or speed it up: change every \\blk{5} and "
         "\\blk{-5} in the loop to a number you like.",
         "Bigger steps move faster; smaller steps are easier to control."),
    ],
)


# ---- Project 2: grab the coin and score --------------------------------------

p2 = BUILD(
    "Grab it, score up",
    goal="Make a \\blk{score}. When the player touches the coin, the score goes "
         "up by one and the coin jumps to a fresh random spot, ready to be "
         "caught again.",
    setup="Make a variable \\textbf{score} \\emph{For all sprites} (Variables "
          "blocks, \\emph{Make a Variable}). It will show in the top-left of the "
          "stage.",
    new_blocks=[
        ("if <touching [Coin]?>", "True when the player is touching the coin. Here it is on the Coin, so it checks touching the Player."),
    ],
    steps=[
        "On the \\textbf{Player}, in the \\blk{when green flag clicked} script, "
        "add \\blk{set [score] to (0)} near the top, before the forever loop.",
        "Now click the \\textbf{Coin} and add a new script: \\blk{when green "
        "flag clicked} then a \\blk{forever} loop.",
        "Inside the loop, add \\blk{if <touching [Player]?>}. That is when the "
        "coin has been caught.",
        "Inside that \\blk{if}, the two blocks are \\blk{? your turn}: first add "
        "a point to the score, then send the coin to a new random spot.",
        "Green flag, and chase the coin. Each catch adds one and the coin hops "
        "away.",
    ],
    script_intro="The Coin's catch loop. Both blocks inside the \\blk{if} are "
                 "yours to fill:",
    scripts=script(
        when_flag(),
        forever(
            if_(touching("Player"),
                gap("add 1 to the score",
                    change_var("score", 1)),
                gap("send the coin to a new random spot",
                    goto_xy(pick_random(-200, 200), pick_random(-140, 140))),
                ),
        ),
        caption="Coin: catch and re-spawn",
    ),
    note="Setting \\blk{score} to 0 on the Player's green-flag script means every "
         "new game starts from zero. The coin's job is only to add points.",
    tasks=[
        ("Give catching a sound: on the Coin, click the \\emph{Sounds} tab, add "
         "a \\emph{Coin} or \\emph{Pop} sound, then put \\blk{start sound [Pop]} "
         "as the first block inside the \\blk{if}.",
         "A sound plays the instant the coin is caught."),
        ("Make some coins worth more: change the point block to \\blk{change "
         "[score] by (pick random (1) to (3))}.",
         "Each catch is now worth 1, 2, or 3 points at random."),
    ],
)


# ---- Project 3: beat the clock -----------------------------------------------

p3 = BUILD(
    "Mini project: beat the clock",
    goal="Add a countdown. A \\blk{time} variable starts at 30 and drops by one "
         "each second. When it reaches zero the game stops, and your final "
         "\\blk{score} is your result.",
    setup="Make a second variable \\textbf{time} \\emph{For all sprites}. You "
          "will build the countdown as a new script on the \\textbf{Player}.",
    new_blocks=[
        ("if <(time) = (0)>", "True the moment the countdown reaches zero. It compares the time variable with 0."),
    ],
    steps=[
        "On the \\textbf{Player}, add a new script: \\blk{when green flag "
        "clicked} then \\blk{set [time] to (30)}.",
        "Add a \\blk{forever} loop. Its first block is \\blk{wait (1) seconds}, "
        "so the loop ticks once a second.",
        "The next block is \\blk{? your turn}: count the time down by one on "
        "every tick.",
        "The last block is an \\blk{if} that ends the game. Its shell and its "
        "inside blocks (\\blk{say (Time up!)} and \\blk{stop [all]}) are given. "
        "The \\blk{? your turn} is the grey hexagon: fill in the test that checks "
        "the time has reached zero.",
        "Green flag. Grab as many coins as you can before the clock runs out.",
    ],
    script_intro="The countdown loop. Fill the grey stack block and the grey "
                 "hexagon in the \\blk{if}:",
    scripts=script(
        when_flag(),
        set_var("time", 30),
        forever(
            wait(1),
            gap("count the time down by 1",
                change_var("time", -1)),
            if_(gap("is the time 0?", eq(var("time"), 0)),
                say_for("Time up!", 2),
                stop_all()),
        ),
        caption="Player: the 30-second countdown",
    ),
    note="The countdown lives in its own forever loop with \\blk{wait (1) "
         "seconds}, so it ticks steadily while your other loops handle moving "
         "and catching at full speed.",
    tasks=[
        ("Show a start message: on the Player, add \\blk{say (Catch the coins!) "
         "for (2) seconds} right after \\blk{set [time] to (30)}.",
         "The player explains the goal at the start of each game."),
        ("Keep a high score. Make a variable \\blk{best}. Just before "
         "\\blk{stop [all]}, add \\blk{if <(score) $>$ (best)>} then \\blk{set "
         "[best] to (score)}.",
         "The best score so far stays on screen across games."),
        ("Add more time for a longer game: change \\blk{set [time] to (30)} to a "
         "bigger number, like 60.",
         "A longer countdown means a higher possible score."),
    ],
)


ACTIVITIES = [p1, p2, p3]
