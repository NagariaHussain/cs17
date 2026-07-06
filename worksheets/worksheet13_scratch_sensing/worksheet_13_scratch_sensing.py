"""Scratch B - Sensing & Choices: the cat reacts to the world.

Scratch A built the basics: sequence, key/click events, a forever loop. Now the
cat starts to *decide*. The new power is the orange Control \\blk{if} and
\\blk{if-else} blocks, steered by light-blue Sensing hexagons (\\blk{touching ()?},
\\blk{touching color ()?}, \\blk{key () pressed?}) and \\blk{point towards}. Each
project is still a small, finished thing the student builds and plays.

  Project 1  point towards + forever   the cat chases the mouse pointer
  Project 2  if + touching edge        it walks, and turns when it hits a wall
  Project 3  if-else + touching color  hot-lava floor: touch red, jump to start
  Project 4  capstone                  flee the mouse, dash on space, react to walls

No variables yet (that is Scratch C) - this sheet is about *choosing* what to do.
"""

from gens.scratchgen import (
    BUILD, script,
    when_flag, when_clicked,
    move, turn_right, point, point_towards, goto_xy, glide_to,
    bounce, set_rotation_style,
    say, say_for, next_costume, play_sound, wait, forever,
    if_, ifelse, touching, touching_color, key_pressed, distance_to, lt,
)

TITLE = "Scratch B"

# only the groups this sheet uses (adds Sensing to the basic set)
PALETTE = ["Motion", "Looks", "Sound", "Events", "Control", "Sensing"]

LEAD = (
    r"\textbf{Welcome back.}\quad In \emph{Scratch A} you built scripts that run "
    r"top to bottom, scripts that start on a key or a click, and a \blk{forever} "
    r"loop that animates the cat. In \emph{Scratch B} the cat starts to "
    r"\emph{make choices}: it looks at the world with light-blue \emph{Sensing} "
    r"blocks and then decides what to do with the orange \blk{if} and "
    r"\blk{if-else} blocks. Open \texttt{scratch.mit.edu}, click \emph{Create}, "
    r"and let us teach the cat to react.")


# ---- Project 1: point towards + forever - chase the mouse --------------------

p1 = BUILD(
    "Chase the mouse",
    goal="The cat follows your mouse pointer wherever it goes. A forever loop "
         "keeps pointing the cat at the pointer and stepping toward it, so it "
         "chases you around the stage.",
    setup="Open a new project. The cat starts in the middle.",
    new_blocks=[
        ("point towards [mouse-pointer]", "A blue Motion block. It turns the sprite to face the pointer (or another sprite)."),
        ("move () steps", "Steps in the direction the sprite is now facing."),
    ],
    steps=[
        "Start a script with \\blk{when green flag clicked}.",
        "From the orange Control blocks, drag in \\blk{forever}.",
        "Inside the forever, add \\blk{point towards [mouse-pointer]} from the "
        "blue Motion blocks. Click the little arrow and choose \\textbf{mouse-pointer}.",
        "Under it, still inside the loop, add \\blk{move (5) steps}.",
        "Click the green flag and move your mouse. The cat chases the pointer.",
    ],
    scripts=script(
        when_flag(),
        forever(
            point_towards("mouse-pointer"),
            move(5),
        ),
    ),
    note="The loop runs many times a second: each time it re-aims at the pointer "
         "and takes one small step, so the cat curves smoothly after your mouse.",
    tasks=[
        ("Make the cat chase faster: change \\blk{move (5) steps} to a bigger "
         "number like 10.", "Bigger steps make the cat catch up quicker."),
        ("Swap \\blk{move (5) steps} for \\blk{glide (0.3) secs to [mouse-pointer]} "
         "so the cat slides smoothly instead of stepping.",
         "The cat glides toward the pointer each loop instead of jumping a step."),
        ("Make the cat speak when it reaches you: inside the loop add "
         "\\blk{if <distance to [mouse-pointer] $<$ (30)>} then \\blk{say (Got you!) "
         "for (0.5) seconds}.",
         "When the pointer is within 30 steps, the cat says Got you!"),
    ],
)


# ---- Project 2: if + touching edge - turn at the wall ------------------------

p2 = BUILD(
    "Turn at the wall",
    goal="The cat walks on its own. Every step it asks one question: am I "
         "touching the edge? If the answer is yes, it turns around and says "
         "ouch. This is your first \\blk{if} block - a choice the program makes.",
    new_blocks=[
        ("if <> then", "An orange Control block. The blocks inside it run only when the hexagon question is true."),
        ("touching [edge]?", "A light-blue Sensing hexagon. It is true when the sprite touches the thing you pick."),
    ],
    steps=[
        "Start with \\blk{when green flag clicked}, then \\blk{set rotation style "
        "[left-right]} and \\blk{point in direction (90)} so the cat faces right "
        "and never flips upside down.",
        "Add a \\blk{forever} loop.",
        "Inside it, add \\blk{move (5) steps}.",
        "From the Control blocks, drag in \\blk{if <> then} under the move block.",
        "Drop \\blk{touching [edge]?} (a Sensing hexagon) into the if's slot.",
        "Inside the if, put \\blk{say (Ouch!) for (0.5) seconds} and "
        "\\blk{turn \\textrightarrow\\ (180) degrees}.",
        "Click the green flag. The cat walks to a wall, says ouch, and turns back.",
    ],
    scripts=script(
        when_flag(),
        set_rotation_style("left-right"),
        point(90),
        forever(
            move(5),
            if_(touching("edge"),
                say_for("Ouch!", 0.5),
                turn_right(180),
            ),
        ),
    ),
    note="A hexagon block is a question with a yes/no answer. It only fits in the "
         "pointy hexagon slot of an \\blk{if} (or another question), never on its own.",
    tasks=[
        ("Add a sound on the bump: inside the if, before the turn, add "
         "\\blk{start sound [Boing]}.", "The cat plays Boing each time it hits a wall."),
        ("Make it change pose on the bump too: add \\blk{next costume} inside the if.",
         "The cat swaps costume every time it turns around."),
        ("Speed the cat up to bump more often: change \\blk{move (5) steps} to "
         "\\blk{move (10) steps}.", "It reaches the walls faster and turns more often."),
    ],
)


# ---- Project 3: if-else + touching color - hot lava --------------------------

p3 = BUILD(
    "The floor is lava",
    goal="A red stripe on the stage is hot lava. The cat walks back and forth, "
         "but every step it chooses: if it is touching red, jump back to the "
         "start and shout; otherwise, keep walking. That is an \\blk{if-else} - "
         "two paths, and the program picks one.",
    setup="Click the \\emph{Stage} thumbnail (bottom right), then the "
          "\\emph{Backdrops} tab. Use the rectangle tool to paint a wide "
          "\\textbf{red} stripe across the floor. That stripe is the lava.",
    new_blocks=[
        ("if <> then ... else ...", "Runs the first stack when the question is true, and the second (else) stack when it is false."),
        ("touching color [ ]?", "A Sensing hexagon. True when the sprite touches that exact colour. Click the colour patch to pick red."),
    ],
    steps=[
        "Start with \\blk{when green flag clicked}, then \\blk{set rotation style "
        "[left-right]}, \\blk{go to x: -200 y: -120}, and \\blk{point in "
        "direction (90)}.",
        "Add a \\blk{forever} loop, and inside it \\blk{move (4) steps}.",
        "Under the move, drag in \\blk{if <> then ... else ...}.",
        "Drop \\blk{touching color [red]?} into its slot. Click the colour patch "
        "on the block and pick the same red as your stripe.",
        "In the \\textbf{if} (true) part, put \\blk{say (Hot lava!) for (0.4) "
        "seconds} and \\blk{go to x: -200 y: -120}.",
        "In the \\textbf{else} (false) part, put \\blk{if on edge, bounce} so the "
        "cat turns around at the ends when it is safe.",
        "Click the green flag. The cat paces the floor; step on red and it leaps "
        "back to the start.",
    ],
    scripts=script(
        when_flag(),
        set_rotation_style("left-right"),
        goto_xy(-200, -120),
        point(90),
        forever(
            move(4),
            ifelse(touching_color("red"),
                   [say_for("Hot lava!", 0.4), goto_xy(-200, -120)],
                   [bounce()]),
        ),
    ),
    note="\\blk{if} runs its blocks only when the answer is yes. \\blk{if-else} "
         "always runs exactly one of its two stacks - never both, never neither.",
    tasks=[
        ("Recolour the lava: paint your stripe a new colour, then click the patch "
         "in \\blk{touching color} and pick that colour to match.",
         "The cat only resets on the colour you chose in the block."),
        ("Animate the safe walk: in the \\textbf{else} part, add \\blk{next "
         "costume} so the legs move while the cat is safe.",
         "The cat animates its walk except when it is on the lava."),
        ("Make it harder: paint a second red stripe somewhere else. The same "
         "block already checks for red, so both stripes are now lava.",
         "Touching either stripe sends the cat back to the start."),
    ],
)


# ---- Project 4: capstone - flee, dash, react --------------------------------

p4 = BUILD(
    "Mini project: catch me if you can",
    goal="Put your new choices together into a little game. The cat runs away "
         "from your mouse, bounces off walls, and dashes when you press the space "
         "bar. Click it and it gives up. Three sensing questions, all in one "
         "forever loop.",
    setup="A new project, cat in the middle. You will build one main script and "
          "one little click script.",
    new_blocks=[
        ("key [space] pressed?", "A Sensing hexagon. True while you hold that key down."),
    ],
    steps=[
        "Build the main script: \\blk{when green flag clicked}, then \\blk{set "
        "rotation style [left-right]}, then a \\blk{forever} loop.",
        "Inside the loop, add \\blk{point towards [mouse-pointer]} then "
        "\\blk{move (-4) steps}. A negative number moves the cat \\emph{away} "
        "from where it faces, so it flees the pointer.",
        "Still inside the loop, add \\blk{if <touching [edge]?>} then "
        "\\blk{if on edge, bounce}, so it does not get stuck on a wall.",
        "Add one more choice in the loop: \\blk{if <key [space] pressed?>} then "
        "\\blk{move (-30) steps} and \\blk{say (Zoom!) for (0.3) seconds} - a "
        "dash when you press space.",
        "Make the second script: \\blk{when this sprite clicked}, then "
        "\\blk{say (You caught me!) for (1) seconds} and \\blk{next costume}.",
        "Green flag. Chase the cat with your mouse, press space to make it dash, "
        "and click it to win.",
    ],
    script_intro="Your main script (left) and the click script (right):",
    scripts=[
        script(
            when_flag(),
            set_rotation_style("left-right"),
            forever(
                point_towards("mouse-pointer"),
                move(-4),
                if_(touching("edge"), bounce()),
                if_(key_pressed("space"), move(-30), say_for("Zoom!", 0.3)),
            ),
            caption="Flee, bounce, and dash",
        ),
        script(
            when_clicked(),
            say_for("You caught me!", 1),
            next_costume(),
            caption="Click: give up",
        ),
    ],
    tasks=[
        ("Make the cat harder to catch: change \\blk{move (-4) steps} to "
         "\\blk{move (-6) steps}.", "It flees faster, so it is harder to corner."),
        ("Add a second dash key: in the loop add \\blk{if <key [up arrow] "
         "pressed?>} then \\blk{move (-30) steps}.",
         "Now both space and the up arrow trigger a dash."),
        ("Warn the player near a wall: inside the \\blk{if <touching [edge]?>}, "
         "add \\blk{say (Wall!) for (0.3) seconds} before the bounce.",
         "The cat shouts Wall! whenever it reaches the edge."),
    ],
)


ACTIVITIES = [p1, p2, p3, p4]
