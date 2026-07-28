"""Scratch G - Space Invaders: the capstone reference build.

Scratch A-F taught the blocks; the E/F capstones filled gaps in small games.
Scratch G is the big one: a full Space Invaders, shown as a finished reference
build. The new power over the earlier game sheets is *clone coordination* - not
one clone or a handful, but a 55-strong fleet of clones that must march, drop,
and turn as a single organism, steered by shared variables and a broadcast
"conductor". The player shoots back (clones as bullets too), the game is won by
clearing the fleet and lost if it lands, and - the signature trick - the swarm
speeds up as you thin it out.

  Project 1  the ship            drive left/right along the bottom row
  Project 2  shooting            one laser at a time (clones + a state flag)
  Project 3  build the fleet     a 5x11 grid from one custom block + two loops
  Project 4  march as one        the conductor: broadcast a beat the fleet obeys
  Project 5  win, lose, speed-up score, game over, you win, and the famous ramp

By the end the student has a complete arcade game and, more importantly, the one
idea that scales Scratch past toy projects: many clones sharing one brain.
"""

from gens.scratchgen import (
    BUILD, script,
    when_flag, when_key, when_receive, when_clone,
    goto, goto_xy, changex, changey, setx, x_position, y_position,
    show, hide, next_costume,
    play_sound, wait, forever, repeat, if_, stop_all,
    create_clone, delete_clone, broadcast, broadcast_wait,
    define, call_block,
    set_var, change_var, var,
    touching, key_pressed,
    add, sub, mul, div, gt, lt, eq,
)

TITLE = "Scratch G"

PALETTE = ["Motion", "Looks", "Sound", "Events", "Control",
           "Sensing", "Operators", "Variables"]

LEAD = (
    r"\textbf{Welcome to Scratch G - Space Invaders.}\quad This is the capstone: "
    r"a full arcade game, shown here as a \emph{finished reference build} you can "
    r"assemble and then make your own. It pulls together everything - movement, "
    r"variables, conditionals, custom blocks, and \blk{broadcast} - and adds the "
    r"one idea that makes big Scratch projects possible: \textbf{clone "
    r"coordination}. A single \textbf{Invader} sprite stamps out 55 clones, and a "
    r"few shared variables plus a broadcast \emph{beat} make the whole fleet march, "
    r"drop, and turn as one. The rule to say out loud: \emph{if there are lots of "
    r"them on screen, they are clones.} Open \texttt{scratch.mit.edu}, click "
    r"\emph{Create}, and build the invasion. The costumes are in "
    r"\texttt{scratch-invaders/assets/sliced/} (run \texttt{slice\_sprite.py}).")


# ---- Project 1: the ship -----------------------------------------------------

p1 = BUILD(
    "The ship",
    goal="Drive the player ship left and right along the bottom row, and keep it "
         "on the screen. Unlike the Dino, the ship DOES move sideways - but the "
         "fleet will still come down to meet it.",
    setup="Add a \\textbf{Player} sprite and upload \\texttt{ship\\_fighter\\_1} as "
          "its costume. Make a variable \\textbf{score} \\emph{For all sprites}. "
          "The ship lives on one row near the bottom (y = -150).",
    new_blocks=[
        ("if <key () pressed?>", "Reading the keys inside one forever loop moves the ship smoothly, in either direction."),
        ("set x to ()", "A guard: clamp \\blk{x position} back to the edge so the ship can't slide off the stage."),
    ],
    steps=[
        "On the \\textbf{Player}: \\blk{when green flag clicked}, \\blk{show}, "
        "\\blk{go to x: (0) y: (-150)}, then \\blk{set [score] to (0)}.",
        "Add a \\blk{forever} loop. Inside it, two key checks: \\blk{if <key "
        "[left arrow] pressed?>} then \\blk{change x by (-6)}, and the same for "
        "\\textbf{right arrow} with \\blk{change x by (6)}.",
        "Still in the loop, two guards: \\blk{if <(x position) > (220)>} then "
        "\\blk{set x to (220)}, and \\blk{if <(x position) < (-220)>} then "
        "\\blk{set x to (-220)}.",
        "Green flag, and drive with the arrow keys.",
    ],
    scripts=script(
        when_flag(),
        show(),
        goto_xy(0, -150),
        set_var("score", 0),
        forever(
            if_(key_pressed("left arrow"), changex(-6)),
            if_(key_pressed("right arrow"), changex(6)),
            if_(gt(x_position(), 220), setx(220)),
            if_(lt(x_position(), -220), setx(-220)),
        ),
        caption="Player: drive left/right, stay on screen",
    ),
    note="Reading keys with \\blk{if <key () pressed?>} inside a forever loop (not "
         "separate \\blk{when key pressed} hats) is what makes the ship feel "
         "responsive - the same trick Maze Quest used.",
    tasks=[
        ("Tune the feel: if the ship is too slow, raise both moves to (8); too "
         "twitchy, lower them to (4).", "The ship's speed matches your taste."),
        ("Swap the look: try \\texttt{ship\\_delta\\_1} as the costume instead.",
         "The classic arrow-fighter shape."),
    ],
)


# ---- Project 2: shooting -----------------------------------------------------

p2 = BUILD(
    "Shooting",
    goal="Fire a laser upward with the space bar - but only ONE at a time, just "
         "like the 1978 arcade. The laser is a clone; a state flag "
         "\\blk{bulletActive} stops you spraying the screen.",
    setup="Add a \\textbf{Bullet} sprite (costume \\texttt{bullet\\_cyan\\_1}). "
          "Make a variable \\textbf{bulletActive} \\emph{For all sprites}. Start "
          "the sprite hidden - only its clones ever show.",
    new_blocks=[
        ("go to [Player]", "Jump the bullet to the ship's muzzle before cloning, so the shot starts where the ship is."),
        ("create clone of [myself]", "Spawn a copy that runs the \\blk{when I start as a clone} script - your flying laser."),
        ("delete this clone", "A clone's own life: it runs the clone hat, then cleans itself up when the shot is spent."),
    ],
    steps=[
        "On the \\textbf{Bullet}: \\blk{when green flag clicked}, \\blk{hide}, "
        "\\blk{set [bulletActive] to (0)}.",
        "Add \\blk{when [space] key pressed}. Inside \\blk{if <(bulletActive) = "
        "(0)>}: \\blk{set [bulletActive] to (1)}, \\blk{go to [Player]}, "
        "\\blk{create clone of [myself]}, \\blk{start sound [shoot]}.",
        "Add \\blk{when I start as a clone}: \\blk{show}, then a \\blk{forever} "
        "that does \\blk{change y by (10)}; if \\blk{<touching [Invader]?>} set "
        "\\blk{bulletActive} back to (0) and \\blk{delete this clone}; and if the "
        "laser flies off the top \\blk{<(y position) > (180)>}, do the same.",
        "Green flag: fire with space. You get one shot at a time - the next only "
        "after this one lands or leaves the top.",
    ],
    script_intro="The one-shot fire rule (left) and each laser's flight (right):",
    scripts=[
        script(
            when_key("space"),
            if_(eq(var("bulletActive"), 0),
                set_var("bulletActive", 1),
                goto("Player"),
                create_clone("myself"),
                play_sound("shoot")),
            caption="Bullet: fire, but only if none is flying",
        ),
        script(
            when_clone(),
            show(),
            forever(
                changey(10),
                if_(touching("Invader"),
                    set_var("bulletActive", 0),
                    delete_clone()),
                if_(gt(y_position(), 180),
                    set_var("bulletActive", 0),
                    delete_clone()),
            ),
            caption="Bullet: fly up, then clean up",
        ),
    ],
    stack=True,
    note="\\blk{bulletActive} is the same \\emph{state-flag} idea as the Dino's "
         "\\blk{grounded?}: a 0/1 variable that gates an action so it can only "
         "happen when it should.",
    tasks=[
        ("Machine-gun mode: temporarily remove the \\blk{if <(bulletActive) = "
         "(0)>} wrapper and hold space.", "A wall of lasers - now you see why the "
         "flag matters."),
        ("Colour your shot: swap the costume to \\texttt{bullet\\_orange\\_1} or "
         "\\texttt{bullet\\_green\\_1}.", "The laser matches your theme."),
    ],
)


# ---- Project 3: build the fleet ----------------------------------------------

p3 = BUILD(
    "Build the fleet",
    goal="Stamp out the classic 5x11 = 55 invaders from ONE sprite, using a "
         "custom block \\blk{spawn invader (x) (y)} called inside two nested "
         "loops. This is My Blocks with inputs, put to real work.",
    setup="Add an \\textbf{Invader} sprite with two wiggle costumes, e.g. "
          "\\texttt{invader\\_green\\_1} and \\texttt{invader\\_green\\_2}. Make "
          "variables \\textbf{invadersLeft}, \\textbf{invaderDir}, "
          "\\textbf{invaderStep}, \\textbf{row}, \\textbf{col} (all \\emph{For all "
          "sprites}) and, \\emph{For this sprite only}, \\textbf{me}.",
    new_blocks=[
        ("define spawn invader (x) (y)", "Make it under \\emph{My Blocks -> Make a Block}; add two number inputs named x and y. The crimson header is where the block's own steps go."),
        ("go to x: (x) y: (y)", "Position the original at the target spot; the clone is born THERE, so no pile-up."),
    ],
    steps=[
        "Make the block: \\emph{My Blocks -> Make a Block}, name it "
        "\\textbf{spawn invader}, and add two number inputs \\textbf{x} and "
        "\\textbf{y}. Under the \\blk{define} header, add \\blk{go to x: (x) y: "
        "(y)}, \\blk{create clone of [myself]}, \\blk{change [invadersLeft] by "
        "(1)}.",
        "On the same sprite, \\blk{when green flag clicked}: \\blk{set [me] to "
        "(0)} (this original is the conductor, not an invader), \\blk{hide}, and "
        "set \\blk{invaderDir} to (1), \\blk{invaderStep} to (12), "
        "\\blk{invadersLeft} to (0).",
        "Build the grid with two \\blk{repeat} loops: \\blk{set [row] to (0)}, "
        "then \\blk{repeat (5)} rows; inside, \\blk{set [col] to (0)} then "
        "\\blk{repeat (11)} columns calling \\blk{spawn invader (x) (y)} with "
        "x = \\blk{(-200) + (col x 40)} and y = \\blk{(150) - (row x 28)}, then "
        "\\blk{change [col] by (1)}; after the inner loop \\blk{change [row] by "
        "(1)}.",
        "Add the clone hat \\blk{when I start as a clone}: \\blk{set [me] to (1)} "
        "and \\blk{show}. Green flag - 55 invaders appear in formation.",
    ],
    script_intro="The custom block (left), the grid builder (middle), and each "
                 "clone waking up (right):",
    scripts=[
        script(
            define("spawn invader", "x", "y"),
            goto_xy(var("x"), var("y")),
            create_clone("myself"),
            change_var("invadersLeft", 1),
            caption="My Block: stamp one invader, count it",
        ),
        script(
            when_flag(),
            set_var("me", 0),
            hide(),
            set_var("invaderDir", 1),
            set_var("invaderStep", 12),
            set_var("invadersLeft", 0),
            set_var("row", 0),
            repeat(5,
                   set_var("col", 0),
                   repeat(11,
                          call_block("spawn invader",
                                     add(-200, mul(var("col"), 40)),
                                     sub(150, mul(var("row"), 28))),
                          change_var("col", 1)),
                   change_var("row", 1)),
            caption="Conductor: build a 5x11 grid",
        ),
        script(
            when_clone(),
            set_var("me", 1),
            show(),
            caption="Each clone: I am a real invader",
        ),
    ],
    stack=True,
    note="A \\emph{For this sprite only} variable like \\blk{me} is copied into "
         "each clone and then owned by it - 55 separate copies. The hidden "
         "original keeps \\blk{me} = 0; every clone sets its own to 1. That one "
         "line is how the fleet's brain tells itself apart from its body.",
    tasks=[
        ("Rank the rows by colour: in \\blk{spawn invader}, before cloning, "
         "\\blk{switch costume} by \\blk{row} - row 0 \\texttt{invader\\_green}, "
         "row 4 \\texttt{invader\\_yellow}, etc.",
         "Each rank looks different, like the real game."),
        ("Change the formation: try \\blk{repeat (4)} rows of \\blk{repeat (8)} "
         "for a smaller, faster wave.", "A different-sized fleet builds cleanly - "
         "the loops do the work."),
    ],
)


# ---- Project 4: march as one -------------------------------------------------

p4 = BUILD(
    "March as one",
    goal="Make the fleet move as a single organism: a hidden conductor beats a "
         "\\blk{broadcast [march]}, every clone steps once, and if ANY clone "
         "touches the wall the conductor drops the fleet and reverses it. This is "
         "clone coordination - the heart of the project.",
    setup="No new sprites. Add the variable \\textbf{hitEdge} \\emph{For all "
          "sprites}. You will extend the conductor's flag script and add two "
          "\\blk{when I receive} scripts to the Invader.",
    new_blocks=[
        ("broadcast [march] and wait", "Shout the beat and pause until every clone has finished its step - that is what keeps them in lockstep."),
        ("(x position) x (invaderDir)", "One test that catches BOTH walls: going right it means x \\textgreater\\ 215; going left, x \\textless\\ -215."),
    ],
    steps=[
        "At the bottom of the conductor's \\blk{when green flag clicked} script "
        "(under the grid loops), add a \\blk{forever}. Its blocks: \\blk{wait} for "
        "\\blk{(0.05) + (invadersLeft / 120)} seconds, then \\blk{set [hitEdge] to "
        "(0)} and \\blk{broadcast [march] and wait}.",
        "Still in that loop: \\blk{if <(hitEdge) = (1)>} then \\blk{broadcast "
        "[dropdown] and wait} and \\blk{set [invaderDir] to ((0) - "
        "(invaderDir))}.",
        "On the Invader, add \\blk{when I receive [march]}. Guard everything with "
        "\\blk{if <(me) = (1)>}. Inside: \\blk{change x by} the amount "
        "\\blk{(invaderDir) x (invaderStep)}, then \\blk{next costume}. Below "
        "those, \\blk{if} the edge test \\blk{(x position) x (invaderDir) > (215)} "
        "is true, \\blk{set [hitEdge] to (1)}.",
        "Add \\blk{when I receive [dropdown]}, also guarded by \\blk{me}: "
        "\\blk{change y by (-16)}.",
        "Green flag: the fleet marches, wiggles, and reverses at each wall.",
    ],
    script_intro="The conductor's heartbeat (left), and the two beats each invader "
                 "obeys (right):",
    scripts=[
        script(
            when_flag(),
            forever(
                wait(add(0.05, div(var("invadersLeft"), 120))),
                set_var("hitEdge", 0),
                broadcast_wait("march"),
                if_(eq(var("hitEdge"), 1),
                    broadcast_wait("dropdown"),
                    set_var("invaderDir", sub(0, var("invaderDir")))),
            ),
            caption="Conductor: beat the march (add under the grid loops)",
        ),
        script(
            when_receive("march"),
            if_(eq(var("me"), 1),
                changex(mul(var("invaderDir"), var("invaderStep"))),
                next_costume(),
                if_(gt(mul(x_position(), var("invaderDir")), 215),
                    set_var("hitEdge", 1))),
            caption="Every invader: step, wiggle, watch the wall",
        ),
        script(
            when_receive("dropdown"),
            if_(eq(var("me"), 1),
                changey(-16)),
            caption="Every invader: drop a row",
        ),
    ],
    stack=True,
    note="Any ONE clone setting \\blk{hitEdge} is enough - the conductor reverses "
         "the WHOLE fleet once, on the next beat. If instead each clone flipped "
         "\\blk{invaderDir} itself, all 55 would fight and jitter. Coordination "
         "through a shared variable is the lesson.",
    tasks=[
        ("Faster fleet: lower \\blk{invaderStep} to (8) for finer steps, or raise "
         "it to (16) for lurching jumps.", "The march feel changes with one "
         "number."),
        ("Bigger drops: change \\blk{change y by (-16)} to (-24) so the fleet "
         "closes in faster.", "Each wall bounce brings them down harder."),
    ],
)


# ---- Project 5: win, lose, and the speed-up ----------------------------------

p5 = BUILD(
    "Win, lose, and the famous speed-up",
    goal="Finish the game: shoot invaders for points, win by clearing them, lose "
         "if they reach you or land - and feel the swarm accelerate as it thins. "
         "That speed-up is one line, and it is the most iconic bug in arcade "
         "history, copied on purpose.",
    setup="Add two text sprites: \\textbf{GameOver} (\\texttt{text\\_game\\_over}) "
          "and \\textbf{YouWin} (\\texttt{text\\_you\\_win}), both hidden at the "
          "start. Everything else is scripts on sprites you already have.",
    new_blocks=[
        ("touching [Bullet]?", "Each invader watches for a laser; when hit it scores, counts down, and removes itself."),
        ("(invadersLeft) = (0)", "The win check - the same count that drives the speed-up also ends the game."),
    ],
    steps=[
        "On the Invader, add a second \\blk{when I start as a clone} with a "
        "\\blk{forever}: \\blk{if <touching [Bullet]?>} then \\blk{change [score] "
        "by (10)}, \\blk{change [invadersLeft] by (-1)}, \\blk{start sound "
        "[invader die]}, \\blk{delete this clone}; and \\blk{if <touching "
        "[Player]?>} then \\blk{broadcast [game over]}.",
        "In the \\blk{when I receive [dropdown]} script, after the drop add "
        "\\blk{if <(y position) < (-120)>} then \\blk{broadcast [game over]} - the "
        "fleet has landed.",
        "In the conductor's heartbeat, at the bottom of the loop, add \\blk{if "
        "<(invadersLeft) = (0)>} then \\blk{broadcast [you win]} and \\blk{stop "
        "[all]}.",
        "On the \\textbf{Player}, add a \\blk{forever} that does \\blk{if "
        "<touching [Invader]?>} then \\blk{broadcast [game over]}.",
        "On \\textbf{GameOver} and \\textbf{YouWin}: \\blk{when green flag "
        "clicked} \\blk{hide}; and \\blk{when I receive [game over]} / \\blk{[you "
        "win]} \\blk{go to x: (0) y: (0)}, \\blk{show}, \\blk{stop [all]}.",
        "Green flag. Clear the fleet to win; let it touch you or land to lose - "
        "and notice the last few invaders are terrifyingly fast.",
    ],
    script_intro="An invader taking a hit (left), the ship's loss check (middle), "
                 "and the win screen (right):",
    scripts=[
        script(
            when_clone(),
            forever(
                if_(touching("Bullet"),
                    change_var("score", 10),
                    change_var("invadersLeft", -1),
                    play_sound("invader die"),
                    delete_clone()),
                if_(touching("Player"),
                    broadcast("game over")),
            ),
            caption="Each invader: hit by a laser -> score and vanish",
        ),
        script(
            when_flag(),
            forever(
                if_(touching("Invader"),
                    broadcast("game over")),
            ),
            caption="Player: touched by the fleet -> lose",
        ),
        script(
            when_receive("you win"),
            goto_xy(0, 0),
            show(),
            stop_all(),
            caption="YouWin: show the banner",
        ),
    ],
    stack=True,
    note="The speed-up is the \\blk{wait ((0.05) + (invadersLeft / 120))} in the "
         "conductor: 55 invaders wait about half a second between beats; the last "
         "one waits a fifth of that. In 1978 this was an accident - the hardware "
         "drew fewer sprites faster - and it became the best difficulty curve in "
         "games. Here it is the same count that decides the win, reused for free.",
    tasks=[
        ("Return fire: add a \\textbf{Bomb} sprite. In an invader's loop, "
         "rarely (\\blk{if <(pick random (1) to (400)) = (1)>}) \\blk{go to} "
         "itself and \\blk{create clone of [Bomb]}; the bomb clone falls until it "
         "hits the Player.", "Now the fleet shoots back."),
        ("Bonus mothership: add a \\textbf{UFO} (\\texttt{ufo\\_purple}) that "
         "slides across the top every 20 seconds for bonus points if you tag it.",
         "A high-value target crosses the sky - pure Dino-style world-slide."),
        ("Rank scoring: give each invader a \\emph{this sprite only} "
         "\\blk{rank} set from \\blk{row} at spawn, and score \\blk{(10) + ((4) - "
         "(rank)) x (10)} so the back rows pay more.",
         "The scariest back row is worth 50; the front row 10."),
    ],
)


ACTIVITIES = [p1, p2, p3, p4, p5]
