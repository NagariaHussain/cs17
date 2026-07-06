"""Scratch D - A Complete Game: build Maze Quest, one piece at a time.

Scratch A, B, and C each built tiny finished projects. Scratch D is different:
the four projects are four stages of ONE bigger game - a maze the player steers
through without touching the walls, racing a patrolling enemy to reach the goal.
The new power is the gold \\blk{broadcast} / \\blk{when I receive} pair: a message
one sprite shouts and others hear, which is how separate sprites and the stage
work together (winning, losing, switching screens).

  Project 1  the maze & the walls    steer the player; touch a wall, back to start
  Project 2  the goal & winning      reach the goal -> broadcast win -> win screen
  Project 3  the enemy & losing      a patrolling enemy + a lives counter
  Project 4  screens & the game loop  a title screen and start/win/lose with broadcasts

By the end the student has a real game with multiple sprites, a score, win and
lose states, and screens - assembled from everything across Scratch A to D.
"""

from gens.scratchgen import (
    BUILD, script,
    when_flag, when_key, when_receive,
    move, point, goto_xy, changex, changey, glide, set_size,
    say_for, switch_backdrop, show, hide, play_sound, wait, forever,
    if_, stop_all, broadcast,
    set_var, change_var, var,
    touching, touching_color, key_pressed, eq,
)

TITLE = "Scratch D"

PALETTE = ["Motion", "Looks", "Sound", "Events", "Control",
           "Sensing", "Operators", "Variables"]

LEAD = (
    r"\textbf{Welcome to Scratch D - the big one.}\quad The last three sheets "
    r"each built a small finished project. This time the four projects are four "
    r"stages of \emph{one} game: \textbf{Maze Quest}. You steer a player through "
    r"a maze without touching the walls, dodge a roaming enemy, and race to the "
    r"goal. The new idea that ties many sprites together is the gold "
    r"\blk{broadcast} message and its partner \blk{when I receive}: one sprite "
    r"shouts a message, and every sprite (and the stage) that is listening "
    r"reacts. That is how a game wins, loses, and changes screens. Open "
    r"\texttt{scratch.mit.edu}, click \emph{Create}, and let us build it.")


# ---- Project 1: the maze and the walls ---------------------------------------

p1 = BUILD(
    "The maze and the walls",
    goal="Draw a maze and steer the player through it. The walls are electric: "
         "if the player touches the wall colour, it jumps back to the start. One "
         "forever loop reads the arrow keys and watches for walls.",
    setup="Click the \\emph{Stage}, then \\emph{Backdrops}, and paint a maze: "
          "thick \\textbf{black} walls with a clear path from the bottom-left "
          "\\emph{start} to the top-right. Rename the cat sprite to "
          "\\textbf{Player} (click its name and retype). The player is small, so "
          "it fits the corridors.",
    new_blocks=[
        ("touching color [black]?", "True when the player touches the wall colour. Click the patch and pick your wall colour."),
        ("if <key [] pressed?> then change x/y", "Reading the four arrow keys inside one forever loop steers the sprite smoothly."),
    ],
    steps=[
        "On the Player, start with \\blk{when green flag clicked}, then "
        "\\blk{set size to (40) \\%} and \\blk{go to x: -210 y: -150} (your "
        "start corner).",
        "Add a \\blk{forever} loop.",
        "Inside it, add four choices, one per arrow key: \\blk{if <key [right "
        "arrow] pressed?>} then \\blk{change x by (3)}; the same for \\textbf{left "
        "arrow} with \\blk{change x by (-3)}, \\textbf{up arrow} with \\blk{change "
        "y by (3)}, and \\textbf{down arrow} with \\blk{change y by (-3)}.",
        "Below those, still in the loop, add \\blk{if <touching color [black]?>} "
        "then \\blk{say (Oops!) for (0.3) seconds} and \\blk{go to x: -210 "
        "y: -150}.",
        "Green flag, and steer with the arrow keys. Brush a wall and you snap "
        "back to the start.",
    ],
    scripts=script(
        when_flag(),
        set_size(40),
        goto_xy(-210, -150),
        forever(
            if_(key_pressed("right arrow"), changex(3)),
            if_(key_pressed("left arrow"), changex(-3)),
            if_(key_pressed("up arrow"), changey(3)),
            if_(key_pressed("down arrow"), changey(-3)),
            if_(touching_color("black"),
                say_for("Oops!", 0.3),
                goto_xy(-210, -150)),
        ),
    ),
    note="Reading keys with \\blk{if <key () pressed?>} inside a forever loop "
         "(instead of separate \\blk{when key pressed} scripts) lets the player "
         "move diagonally and feels much smoother in a maze.",
    tasks=[
        ("Match your walls: click the colour patch in \\blk{touching color} and "
         "pick the exact colour you painted the walls.",
         "The player only resets on your real wall colour."),
        ("Tune the speed: if the player slips through thin walls, lower the moves "
         "to (2); if it feels sluggish, raise them to (4).",
         "Smaller steps are more precise; larger steps are faster."),
        ("Add a start label: after \\blk{go to x: -210 y: -150} in the flag "
         "script, add \\blk{say (Reach the top-right!)}.",
         "The player explains the goal at the start of each run."),
    ],
)


# ---- Project 2: the goal and winning (broadcast) -----------------------------

p2 = BUILD(
    "The goal and winning",
    goal="Add a goal to reach. When the player touches it, it shouts a "
         "\\blk{broadcast [win]} message. The stage hears it and switches to a "
         "win screen, and the goal hears it and cheers. One message, two "
         "listeners - that is how sprites work as a team.",
    setup="Add a \\textbf{Goal} sprite (click \\emph{Choose a Sprite}, pick a "
          "star or ball, rename it \\textbf{Goal}) and drag it to the top-right "
          "of the maze. Add a second backdrop and paint \\emph{YOU WIN} on it; "
          "name that backdrop \\textbf{win}.",
    new_blocks=[
        ("broadcast [win]", "A gold Events block. It shouts a message to every sprite and the stage at once."),
        ("when I receive [win]", "A gold hat. The script under it runs when that message is shouted."),
        ("switch backdrop to [win]", "Change the stage picture - here, to the win screen."),
    ],
    steps=[
        "On the \\textbf{Player}, inside the forever loop, add \\blk{if "
        "<touching [Goal]?>} then \\blk{broadcast [win]}. Click the arrow in the "
        "broadcast block and choose \\emph{New message}, name it \\textbf{win}.",
        "On the \\textbf{Goal}, add a new script: \\blk{when I receive [win]}, "
        "then \\blk{say (You made it!) for (2) seconds} and \\blk{stop [all]}.",
        "On the \\textbf{Stage}, add \\blk{when I receive [win]} then "
        "\\blk{switch backdrop to [win]}.",
        "Green flag, steer to the goal. The win screen appears, the goal cheers, "
        "and the game stops.",
    ],
    script_intro="One message, two listeners - the Goal (left) and the Stage (right):",
    scripts=[
        script(
            when_receive("win"),
            say_for("You made it!", 2),
            stop_all(),
            caption="On the Goal sprite",
        ),
        script(
            when_receive("win"),
            switch_backdrop("win"),
            caption="On the Stage",
        ),
    ],
    note="\\blk{broadcast} does not say who should react - it just shouts. Any "
         "sprite with a matching \\blk{when I receive} hat answers. Add more "
         "listeners any time without touching the sprite that broadcasts.",
    tasks=[
        ("Give winning a sound: on the Goal, add \\blk{start sound [Cheer]} "
         "before the say block in the \\blk{when I receive [win]} script.",
         "A cheer plays the moment the player wins."),
        ("Make the goal inviting: add a \\blk{when green flag clicked} script on "
         "the Goal with a \\blk{forever} loop that does \\blk{change size by (5)}, "
         "\\blk{wait (0.1) seconds}, \\blk{change size by (-5)}, so it pulses.",
         "The goal gently grows and shrinks to draw the eye."),
        ("Hide the win screen at the start: on the Stage, add \\blk{when green "
         "flag clicked} then \\blk{switch backdrop to [maze]} so each new game "
         "begins on the maze.", "The maze always shows first; the win screen only on a win."),
    ],
)


# ---- Project 3: the enemy and losing -----------------------------------------

p3 = BUILD(
    "The enemy and losing",
    goal="Add danger. A patrolling enemy slides up and down the maze, and a "
         "\\blk{lives} counter starts at 3. Touch the enemy and you lose a life "
         "and restart; run out of lives and the game broadcasts \\blk{lose}.",
    setup="Add an \\textbf{Enemy} sprite (rename it \\textbf{Enemy}) and place it "
          "on the path. Make a variable \\textbf{lives} \\emph{For all sprites}. "
          "Add a backdrop with \\emph{GAME OVER} painted on it, named "
          "\\textbf{lose}.",
    new_blocks=[
        ("glide () secs to x: () y: ()", "Slides the sprite smoothly to a spot over a set time - perfect for a patrol."),
        ("broadcast [lose]", "A second message, shouted when the player runs out of lives."),
    ],
    steps=[
        "On the \\textbf{Enemy}, make it patrol: \\blk{when green flag clicked}, "
        "then a \\blk{forever} loop with \\blk{glide (1) secs to x: (100) y: "
        "(120)} and \\blk{glide (1) secs to x: (100) y: (-120)}.",
        "On the \\textbf{Player}, in the \\blk{when green flag clicked} script "
        "(before the loop), add \\blk{set [lives] to (3)}.",
        "In the Player's forever loop, add \\blk{if <touching [Enemy]?>} then "
        "\\blk{change [lives] by (-1)}, \\blk{go to x: -210 y: -150}, and "
        "\\blk{wait (0.5) seconds}.",
        "Just below that, still in the loop, add \\blk{if <(lives) = (0)>} then "
        "\\blk{broadcast [lose]}. Make the new \\textbf{lose} message.",
        "On the \\textbf{Stage}, add \\blk{when I receive [lose]} then "
        "\\blk{switch backdrop to [lose]} and \\blk{stop [all]}.",
        "Green flag. Dodge the enemy - three touches and it is game over.",
    ],
    script_intro="The enemy's patrol (left) and the Stage's lose handler (right):",
    scripts=[
        script(
            when_flag(),
            forever(
                glide(1, 100, 120),
                glide(1, 100, -120),
            ),
            caption="Enemy: patrol up and down",
        ),
        script(
            when_receive("lose"),
            switch_backdrop("lose"),
            stop_all(),
            caption="Stage: game over",
        ),
    ],
    note="The lives check uses \\blk{(lives) = (0)} - the same green comparison "
         "from Scratch C. When it is true, one \\blk{broadcast [lose]} ends the "
         "game everywhere at once.",
    tasks=[
        ("Show the danger: on the Player, in the touching-Enemy part, add "
         "\\blk{say (Ouch!) for (0.3) seconds} before the restart.",
         "The player reacts each time the enemy catches it."),
        ("Make the enemy faster: change both glide times from (1) to (0.6) "
         "seconds.", "The enemy patrols quicker, so it is harder to slip past."),
        ("Add a second enemy: right-click the Enemy and choose \\emph{duplicate}, "
         "then change the copy's glide x to a different column so it guards "
         "another part of the maze.", "Two enemies patrol different lanes."),
    ],
)


# ---- Project 4: screens and the game loop (game states) ----------------------

p4 = BUILD(
    "Mini project: screens and the game loop",
    goal="Wrap the game in a proper start. A title screen waits for the player; "
         "press space to begin and a \\blk{broadcast [start]} kicks everything "
         "off. Now your game has real states - title, playing, win, lose - all "
         "steered by messages.",
    setup="Add a backdrop with \\emph{MAZE QUEST - press space} painted on it, "
          "named \\textbf{title}. You will move the player's start-up so it waits "
          "for the \\textbf{start} message instead of the green flag.",
    new_blocks=[
        ("when I receive [start]", "Begin play only after the title screen, not the instant the flag is clicked."),
    ],
    steps=[
        "On the \\textbf{Stage}, add \\blk{when green flag clicked} then "
        "\\blk{switch backdrop to [title]}, so every game opens on the title.",
        "On the \\textbf{Player}, add \\blk{when green flag clicked} then "
        "\\blk{hide} (the player waits off-screen on the title).",
        "Add a tiny starter: \\blk{when [space] key pressed} then "
        "\\blk{broadcast [start]} (make the \\textbf{start} message).",
        "Change the Player's set-up to run on the message: \\blk{when I receive "
        "[start]}, then \\blk{show}, \\blk{set [lives] to (3)}, \\blk{go to x: "
        "-210 y: -150}, and the \\blk{forever} movement loop you built in "
        "Projects 1-3.",
        "On the \\textbf{Stage}, in the \\blk{when I receive [start]} script, "
        "\\blk{switch backdrop to [maze]} so play begins on the maze.",
        "Green flag: the title shows. Press space and the maze, player, enemy, "
        "and goal all spring to life. You have a complete game!",
    ],
    script_intro="The title setup (left) and the player starting on the message (right):",
    scripts=[
        script(
            when_flag(),
            switch_backdrop("title"),
            caption="Stage: show the title",
        ),
        script(
            when_receive("start"),
            show(),
            set_var("lives", 3),
            goto_xy(-210, -150),
            caption="Player: begin on start",
        ),
    ],
    note="Messages are the game's traffic controller: \\blk{start} begins play, "
         "\\blk{win} and \\blk{lose} end it. Each sprite just listens for the "
         "messages it cares about - that is how big projects stay organised.",
    tasks=[
        ("Add Level 2: paint a harder maze backdrop named \\textbf{level2}. "
         "Change the Goal's \\blk{when I receive [win]} to \\blk{broadcast "
         "[next]} instead of \\blk{stop [all]}, and add \\blk{when I receive "
         "[next]} handlers that switch the backdrop to \\textbf{level2} and move "
         "the goal.", "Winning loads the next level instead of ending the game."),
        ("Keep a high score: make a variable \\blk{best}. When the player wins, "
         "add \\blk{if <(lives) $>$ (best)>} then \\blk{set [best] to (lives)} so "
         "the best finish is remembered.",
         "The best result so far stays on screen across games."),
        ("Add title music: on the Stage, in \\blk{when green flag clicked}, add "
         "\\blk{start sound [Dance Around]} so the title screen has a tune.",
         "Music plays while the player reads the title."),
    ],
)


ACTIVITIES = [p1, p2, p3, p4]
