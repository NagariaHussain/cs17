"""Scratch G - Space Invaders: the capstone reference build.

Scratch A-F taught the blocks; the E/F capstones filled gaps in small games.
Scratch G is the big one: a full Space Invaders. The new power over the earlier
game sheets is *clone coordination* - not one clone or a handful, but a 55-strong
fleet of clones that must march, drop, and turn as a single organism, steered by
shared variables and a broadcast "conductor".

The sheet builds the game piece by piece: every project ends at a green-flag
checkpoint where the game RUNS, half-built on purpose. The student sees the
problem (lasers spray, the fleet jams into the wall) before building the fix -
each project's goal is "this works; now let's make THIS work".

  Project 1  the ship            drive left/right; then stop it sliding off
  Project 2  fire!               a laser clone flies up (and sprays - on purpose)
  Project 3  one shot at a time  the bulletActive state flag fixes the spray
  Project 4  build the fleet     one invader -> a row -> the 5x11 grid
  Project 5  march!              broadcast a beat; the fleet marches (one way)
  Project 6  bounce and drop     hitEdge: any clone spots the wall, all obey
  Project 7  shoot the fleet     hits, score - and the famous speed-up one-liner
  Project 8  win and lose        banners, landing check, the win condition

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
    r"a full arcade game. It pulls together everything - movement, "
    r"variables, conditionals, custom blocks, and \blk{broadcast} - and adds the "
    r"one idea that makes big Scratch projects possible: \textbf{clone "
    r"coordination}. A single \textbf{Invader} sprite stamps out 55 clones, and a "
    r"few shared variables plus a broadcast \emph{beat} make the whole fleet march, "
    r"drop, and turn as one. The rule to say out loud: \emph{if there are lots of "
    r"them on screen, they are clones.} We build in small steps: after \emph{every} "
    r"project you press the green flag and the game runs - half-built on purpose. "
    r"You will see each problem before you fix it. Open \texttt{scratch.mit.edu}, "
    r"click \emph{Create}, and build the invasion. Your teacher will give you the "
    r"costume images.")


# ---- Project 1: the ship -----------------------------------------------------

p1 = BUILD(
    "The ship",
    goal="Drive the player ship left and right along the bottom row. First make "
         "it move at all - then fix the problem you will see with your own eyes: "
         "it slides right off the stage.",
    setup="Add a \\textbf{Player} sprite and upload \\texttt{ship\\_fighter\\_1} as "
          "its costume. The ship lives on one row near the bottom (y = -150).",
    new_blocks=[
        ("if <key () pressed?>", "Reading the keys inside one forever loop moves the ship smoothly, in either direction."),
        ("set x to ()", "A guard: clamp \\blk{x position} back to the edge so the ship can't slide off the stage."),
    ],
    steps=[
        "On the \\textbf{Player}: \\blk{when green flag clicked}, \\blk{show}, "
        "\\blk{go to x: (0) y: (-150)}.",
        "Add a \\blk{forever} loop. Inside it, two key checks: \\blk{if <key "
        "[left arrow] pressed?>} then \\blk{change x by (-6)}, and the same for "
        "\\textbf{right arrow} with \\blk{change x by (6)}.",
        "\\textbf{Checkpoint} - green flag: drive with the arrow keys. It works! "
        "Now hold a key down... and watch the ship squash itself into the edge. "
        "That is the problem we fix next.",
        "Add two guards to the loop: \\blk{if <(x position) > (220)>} then "
        "\\blk{set x to (220)}, and \\blk{if <(x position) < (-220)>} then "
        "\\blk{set x to (-220)}.",
        "Green flag again: the ship now stops cleanly at each wall.",
    ],
    scripts=script(
        when_flag(),
        show(),
        goto_xy(0, -150),
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


# ---- Project 2: fire! --------------------------------------------------------

p2 = BUILD(
    "Fire!",
    goal="The ship drives - now make it shoot. Press space and a laser clone "
         "flies up from the ship. This version fires as fast as you can mash - "
         "a spray. That is fine for now; seeing the spray IS the point.",
    setup="Add a \\textbf{Bullet} sprite (costume \\texttt{bullet\\_cyan\\_1}). "
          "Start the sprite hidden - only its clones ever show.",
    new_blocks=[
        ("go to [Player]", "Jump the bullet to the ship's muzzle before cloning, so the shot starts where the ship is."),
        ("create clone of [myself]", "Spawn a copy that runs the \\blk{when I start as a clone} script - your flying laser."),
        ("delete this clone", "A clone's own life: it runs the clone hat, then cleans itself up when the shot is spent."),
    ],
    steps=[
        "On the \\textbf{Bullet}: \\blk{when green flag clicked}, \\blk{hide}.",
        "Add \\blk{when [space] key pressed}: \\blk{go to [Player]}, "
        "\\blk{create clone of [myself]}, \\blk{start sound [shoot]}.",
        "Add \\blk{when I start as a clone}: \\blk{show}, then a \\blk{forever} "
        "that does \\blk{change y by (10)}.",
        "\\textbf{Checkpoint} - green flag: press space. A laser flies up from "
        "the ship - and off the top it keeps flying, invisible, forever. Every "
        "shot is a clone that never dies. Fix that:",
        "In the clone's \\blk{forever}, add \\blk{if <(y position) > (180)>} "
        "then \\blk{delete this clone}.",
        "Green flag: each shot now vanishes at the top. But hold space down - a "
        "wall of lasers! The 1978 arcade allowed only ONE shot at a time. That "
        "is the next project.",
    ],
    script_intro="The trigger (left) and each laser's flight (right):",
    scripts=[
        script(
            when_key("space"),
            goto("Player"),
            create_clone("myself"),
            play_sound("shoot"),
            caption="Bullet: fire on space (no limit - yet)",
        ),
        script(
            when_clone(),
            show(),
            forever(
                changey(10),
                if_(gt(y_position(), 180),
                    delete_clone()),
            ),
            caption="Bullet: fly up, vanish off the top",
        ),
    ],
    stack=True,
    note="A clone that flies off the top does not disappear - Scratch keeps it "
         "alive (and counted) until \\blk{delete this clone} runs. Spraying "
         "hundreds of immortal clones is how projects grind to a halt.",
    tasks=[
        ("Colour your shot: swap the costume to \\texttt{bullet\\_orange\\_1} or "
         "\\texttt{bullet\\_green\\_1}.", "The laser matches your theme."),
        ("Faster laser: change \\blk{change y by (10)} to (16).",
         "The shot crosses the screen noticeably quicker."),
    ],
)


# ---- Project 3: one shot at a time -------------------------------------------

p3 = BUILD(
    "One shot at a time",
    goal="Shooting works - too well. Bring in the 1978 rule: only one laser on "
         "screen. A state flag \\blk{bulletActive} gates the trigger, exactly "
         "like the Dino's \\blk{grounded?} gated jumping.",
    setup="Make a variable \\textbf{bulletActive} \\emph{For all sprites}.",
    new_blocks=[
        ("if <(bulletActive) = (0)>", "The gate: fire only when no laser is flying. Set it to 1 when you shoot, back to 0 when the shot is spent."),
    ],
    steps=[
        "In the Bullet's \\blk{when green flag clicked} script, add \\blk{set "
        "[bulletActive] to (0)}.",
        "In the \\blk{when [space] key pressed} script, wrap the three blocks in "
        "\\blk{if <(bulletActive) = (0)>}, and add \\blk{set [bulletActive] to "
        "(1)} as the first block inside.",
        "In the clone's off-the-top check, before \\blk{delete this clone}, add "
        "\\blk{set [bulletActive] to (0)} - the shot is spent, so reload.",
        "\\textbf{Checkpoint} - green flag: hold space down. One laser at a "
        "time; the next fires only after this one leaves the top.",
    ],
    script_intro="All three Bullet scripts, finished:",
    scripts=[
        script(
            when_flag(),
            hide(),
            set_var("bulletActive", 0),
            caption="Bullet: start hidden, gate open",
        ),
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
                if_(gt(y_position(), 180),
                    set_var("bulletActive", 0),
                    delete_clone()),
            ),
            caption="Bullet: fly up, then reload the gate",
        ),
    ],
    stack=True,
    note="\\blk{bulletActive} is a \\emph{state flag}: a 0/1 variable that gates "
         "an action so it can only happen when it should. Every set must have a "
         "matching reset - forget the reset and you can never fire again.",
    tasks=[
        ("Machine-gun experiment: pull the three blocks OUT of the \\blk{if} "
         "wrapper, hold space, watch the spray - then put them back.",
         "You feel exactly what the flag buys you."),
    ],
)


# ---- Project 4: build the fleet ----------------------------------------------

p4 = BUILD(
    "Build the fleet",
    goal="Something to shoot at! Stamp out the classic 5x11 = 55 invaders from "
         "ONE sprite, growing it in three checkpoints: one invader, then a row, "
         "then the grid. The tool is a custom block \\blk{spawn invader (x) (y)}.",
    setup="Add an \\textbf{Invader} sprite with two wiggle costumes, e.g. "
          "\\texttt{invader\\_green\\_1} and \\texttt{invader\\_green\\_2}. Make "
          "variables \\textbf{invadersLeft}, \\textbf{row}, \\textbf{col} (all "
          "\\emph{For all sprites}) and, \\emph{For this sprite only}, "
          "\\textbf{me}.",
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
        "(0)} (this original is the conductor, not an invader), \\blk{hide}, "
        "\\blk{set [invadersLeft] to (0)} - then call \\blk{spawn invader (0) "
        "(150)} once.",
        "Add the clone hat \\blk{when I start as a clone}: \\blk{set [me] to (1)} "
        "and \\blk{show}.",
        "\\textbf{Checkpoint} - green flag: ONE invader appears at the top. The "
        "stamp works.",
        "Now a row. Replace the single call with: \\blk{set [col] to (0)}, then "
        "\\blk{repeat (11)} calling \\blk{spawn invader ((-200) + (col x 40)) "
        "(150)} and \\blk{change [col] by (1)}. Green flag: a row of 11.",
        "Now the grid. Wrap the row code in \\blk{set [row] to (0)} and "
        "\\blk{repeat (5)}, change y to \\blk{(150) - (row x 28)}, and after the "
        "inner loop \\blk{change [row] by (1)}.",
        "\\textbf{Checkpoint} - green flag: 55 invaders in formation.",
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


# ---- Project 5: march! -------------------------------------------------------

p5 = BUILD(
    "March!",
    goal="The fleet stands still - make it move as a single organism. A hidden "
         "conductor beats a \\blk{broadcast [march]}, and every clone steps once "
         "per beat. This version only marches one way - watch what happens when "
         "it meets the wall.",
    setup="No new sprites. Make variables \\textbf{invaderDir} and "
          "\\textbf{invaderStep}, both \\emph{For all sprites}.",
    new_blocks=[
        ("broadcast [march] and wait", "Shout the beat and pause until every clone has finished its step - that is what keeps them in lockstep."),
        ("when I receive [march]", "Each clone's marching orders: one step per beat, guarded by \\blk{me} so the hidden conductor stays put."),
    ],
    steps=[
        "In the conductor's \\blk{when green flag clicked} script, next to the "
        "other \\blk{set} blocks, add \\blk{set [invaderDir] to (1)} and "
        "\\blk{set [invaderStep] to (12)}.",
        "At the bottom of the same script (under the grid loops), add a "
        "\\blk{forever}: \\blk{wait (0.3) seconds}, then \\blk{broadcast [march] "
        "and wait}.",
        "On the Invader, add \\blk{when I receive [march]}. Guard everything "
        "with \\blk{if <(me) = (1)>}. Inside: \\blk{change x by} the amount "
        "\\blk{(invaderDir) x (invaderStep)}, then \\blk{next costume}.",
        "\\textbf{Checkpoint} - green flag: the fleet marches right in perfect "
        "lockstep, wiggling as it goes... and then grinds into the right wall "
        "and jams there. Half-built, as planned - the bounce is next.",
    ],
    script_intro="Add the beat to the conductor (left); every invader obeys it "
                 "(right):",
    scripts=[
        script(
            when_flag(),
            set_var("invaderDir", 1),
            set_var("invaderStep", 12),
            forever(
                wait(0.3),
                broadcast_wait("march"),
            ),
            caption="Conductor: sets at the top, beat under the grid loops",
        ),
        script(
            when_receive("march"),
            if_(eq(var("me"), 1),
                changex(mul(var("invaderDir"), var("invaderStep"))),
                next_costume()),
            caption="Every invader: step and wiggle on the beat",
        ),
    ],
    stack=True,
    note="Why a broadcast beat and not a \\blk{forever} loop on each clone? 55 "
         "independent loops drift apart; one conductor with \\blk{broadcast and "
         "wait} keeps all 55 perfectly in step. One brain, many bodies.",
    tasks=[
        ("March feel: lower \\blk{invaderStep} to (8) for finer steps, or raise "
         "it to (16) for lurching jumps.", "The march feel changes with one "
         "number."),
    ],
)


# ---- Project 6: bounce and drop ----------------------------------------------

p6 = BUILD(
    "Bounce and drop",
    goal="Un-jam the fleet: when ANY clone touches a wall, the whole fleet drops "
         "one row and reverses. One shared variable \\blk{hitEdge} is the "
         "message from the many to the one.",
    setup="Make the variable \\textbf{hitEdge} \\emph{For all sprites}.",
    new_blocks=[
        ("(x position) x (invaderDir)", "One test that catches BOTH walls: going right it means x \\textgreater\\ 215; going left, x \\textless\\ -215."),
    ],
    steps=[
        "In the \\blk{when I receive [march]} script, under \\blk{next costume}, "
        "add \\blk{if <((x position) x (invaderDir)) > (215)>} then \\blk{set "
        "[hitEdge] to (1)}.",
        "In the conductor's beat loop: before the broadcast, \\blk{set [hitEdge] "
        "to (0)}. After it, \\blk{if <(hitEdge) = (1)>} then \\blk{broadcast "
        "[dropdown] and wait} and \\blk{set [invaderDir] to ((0) - "
        "(invaderDir))}.",
        "On the Invader, add \\blk{when I receive [dropdown]}, also guarded by "
        "\\blk{me}: \\blk{change y by (-16)}.",
        "\\textbf{Checkpoint} - green flag: the fleet marches, drops at each "
        "wall, reverses, and slowly closes in. The invasion is on.",
    ],
    script_intro="The conductor's finished heartbeat (left), and the two beats "
                 "each invader obeys (right):",
    scripts=[
        script(
            when_flag(),
            forever(
                wait(0.3),
                set_var("hitEdge", 0),
                broadcast_wait("march"),
                if_(eq(var("hitEdge"), 1),
                    broadcast_wait("dropdown"),
                    set_var("invaderDir", sub(0, var("invaderDir")))),
            ),
            caption="Conductor: the finished heartbeat",
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
        ("Bigger drops: change \\blk{change y by (-16)} to (-24) so the fleet "
         "closes in faster.", "Each wall bounce brings them down harder."),
    ],
)


# ---- Project 7: shoot the fleet ----------------------------------------------

p7 = BUILD(
    "Shoot the fleet",
    goal="The fleet marches and you can shoot - but lasers pass straight "
         "through. Wire up the hits: invaders die for points, and then ONE "
         "changed line gives you the most iconic difficulty curve in arcade "
         "history.",
    setup="Make a variable \\textbf{score} \\emph{For all sprites}.",
    new_blocks=[
        ("touching [Bullet]?", "Each invader watches for a laser; when hit it scores, counts down, and removes itself."),
    ],
    steps=[
        "On the \\textbf{Player}'s \\blk{when green flag clicked} script, add "
        "\\blk{set [score] to (0)}.",
        "On the Invader, add a SECOND \\blk{when I start as a clone} with a "
        "\\blk{forever}: \\blk{if <touching [Bullet]?>} then \\blk{change [score] "
        "by (10)}, \\blk{change [invadersLeft] by (-1)}, \\blk{start sound "
        "[invader die]}, \\blk{delete this clone}.",
        "On the Bullet's clone loop, add a matching check: \\blk{if <touching "
        "[Invader]?>} then \\blk{set [bulletActive] to (0)} and \\blk{delete "
        "this clone} - a hit reloads the gate too, not just the top of the "
        "screen.",
        "\\textbf{Checkpoint} - green flag: shoot the fleet. Invaders vanish, "
        "the score climbs... but the march never changes pace. Time for the "
        "famous one-liner:",
        "In the conductor's heartbeat, replace \\blk{wait (0.3) seconds} with "
        "\\blk{wait ((0.05) + ((invadersLeft) / (120))) seconds}.",
        "Green flag: thin the fleet - the survivors sprint.",
    ],
    script_intro="An invader taking a hit (left), and the Bullet's finished "
                 "flight (right):",
    scripts=[
        script(
            when_clone(),
            forever(
                if_(touching("Bullet"),
                    change_var("score", 10),
                    change_var("invadersLeft", -1),
                    play_sound("invader die"),
                    delete_clone()),
            ),
            caption="Each invader: hit by a laser -> score and vanish",
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
            caption="Bullet: fly up, then clean up (finished)",
        ),
    ],
    stack=True,
    note="The speed-up is the \\blk{wait ((0.05) + (invadersLeft / 120))}: 55 "
         "invaders wait about half a second between beats; the last one waits a "
         "fifth of that. In 1978 this was an accident - the hardware drew fewer "
         "sprites faster - and it became the best difficulty curve in games. You "
         "copied it on purpose, with one line.",
    tasks=[
        ("Rank scoring: give each invader a \\emph{this sprite only} "
         "\\blk{rank} set from \\blk{row} at spawn, and score \\blk{(10) + ((4) - "
         "(rank)) x (10)} so the back rows pay more.",
         "The scariest back row is worth 50; the front row 10."),
    ],
)


# ---- Project 8: win and lose -------------------------------------------------

p8 = BUILD(
    "Win and lose",
    goal="The game plays - now let it END. Win by clearing the fleet; lose if it "
         "reaches you or lands. The win check reuses \\blk{invadersLeft} - the "
         "same count that drives the speed-up decides the victory.",
    setup="Add two text sprites: \\textbf{GameOver} (\\texttt{text\\_game\\_over}) "
          "and \\textbf{YouWin} (\\texttt{text\\_you\\_win}), both hidden at the "
          "start.",
    new_blocks=[
        ("(invadersLeft) = (0)", "The win check - when the count the spawner built up reaches zero, the fleet is gone."),
        ("stop [all]", "Freeze the whole project on the banner - game over means game OVER."),
    ],
    steps=[
        "On \\textbf{GameOver} and \\textbf{YouWin}: \\blk{when green flag "
        "clicked} \\blk{hide}; and \\blk{when I receive [game over]} / \\blk{[you "
        "win]} \\blk{go to x: (0) y: (0)}, \\blk{show}, \\blk{stop [all]}.",
        "On the \\textbf{Player}, add a \\blk{forever} that does \\blk{if "
        "<touching [Invader]?>} then \\blk{broadcast [game over]}.",
        "In the Invader's \\blk{when I receive [dropdown]} script, after the "
        "drop, add \\blk{if <(y position) < (-120)>} then \\blk{broadcast [game "
        "over]} - the fleet has landed.",
        "In the conductor's heartbeat, at the bottom of the loop, add \\blk{if "
        "<(invadersLeft) = (0)>} then \\blk{broadcast [you win]}.",
        "\\textbf{Checkpoint} - green flag, one last time: clear the fleet to "
        "win; let it touch you or land to lose. The game is COMPLETE.",
    ],
    script_intro="The ship's loss check (left) and the win banner (right):",
    scripts=[
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
    note="Three different roads lead to \\blk{broadcast [game over]} - touching "
         "the ship, and the fleet landing - but ONE script shows the banner. "
         "Broadcasts collect all the ways to lose into a single ending.",
    tasks=[
        ("Return fire: add a \\textbf{Bomb} sprite. In an invader's loop, "
         "rarely (\\blk{if <(pick random (1) to (400)) = (1)>}) \\blk{go to} "
         "itself and \\blk{create clone of [Bomb]}; the bomb clone falls until it "
         "hits the Player.", "Now the fleet shoots back."),
        ("Bonus mothership: add a \\textbf{UFO} (\\texttt{ufo\\_purple}) that "
         "slides across the top every 20 seconds for bonus points if you tag it.",
         "A high-value target crosses the sky - pure Dino-style world-slide."),
    ],
)


ACTIVITIES = [p1, p2, p3, p4, p5, p6, p7, p8]
