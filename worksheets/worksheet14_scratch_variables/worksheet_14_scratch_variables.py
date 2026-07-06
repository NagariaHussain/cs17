"""Scratch C - Variables & Score: the cat remembers numbers.

Scratch B taught the cat to *choose* with \\blk{if} / \\blk{if-else}. But a choice
needs something to test, and a game needs a score. Scratch C adds the two groups
that make real games possible: dark-orange \\blk{Variables} (a named box that
remembers a number, like \\blk{score}) and green \\blk{Operators} (maths and
comparisons: \\blk{pick random}, \\blk{() + ()}, \\blk{() $<$ ()}, \\blk{() = ()}).

  Project 1  set / change a variable    a counter that remembers your clicks
  Project 2  pick random + score        whack-a-cat: it pops up, you click to score
  Project 3  ask / answer + repeat until guess-my-number with higher / lower hints
  Project 4  capstone                   catch the falling apple - a real score game

Every project keeps a number and shows it on the stage, so the student can watch
the variable change as the program runs.
"""

from gens.scratchgen import (
    BUILD, script,
    when_flag, when_key, when_clicked,
    goto_xy, changey,
    say, say_for, change_size, play_sound, wait, forever,
    if_, ifelse, repeat_until, stop_all,
    set_var, change_var, var,
    ask, answer, touching,
    pick_random, join, gt, eq,
)

TITLE = "Scratch C"

PALETTE = ["Motion", "Looks", "Sound", "Events", "Control",
           "Sensing", "Operators", "Variables"]

LEAD = (
    r"\textbf{Welcome to Scratch C.}\quad So far the cat could move, react, and "
    r"choose - but it could not \emph{remember} anything. Now it can. A "
    r"\emph{variable} is a named box that holds a number (or a word), like "
    r"\blk{score} or \blk{lives}; you \blk{set} it and \blk{change} it, and its "
    r"value shows live on the stage. Paired with green \emph{Operators} - "
    r"\blk{pick random}, \blk{$+$}, and the comparisons \blk{$<$}, \blk{$=$}, "
    r"\blk{$>$} - variables turn your projects into real games that keep score. "
    r"Open \texttt{scratch.mit.edu} and click \emph{Create}.")


# ---- Project 1: make / set / change a variable - a click counter -------------

p1 = BUILD(
    "A counter that remembers",
    goal="Make your first variable. Every time you click the cat, a number called "
         "\\blk{clicks} goes up by one, and the cat tells you the total. The "
         "variable remembers the count between clicks - that is the whole point.",
    setup="Click the dark-orange \\emph{Variables} group, then \\emph{Make a "
          "Variable}. Name it \\textbf{clicks} and click OK. A little box "
          "appears on the stage showing its value.",
    new_blocks=[
        ("set [clicks] to ()", "Put a number into the variable. Use this to start the count at 0."),
        ("change [clicks] by ()", "Add to the variable. Change by 1 counts up; change by -1 counts down."),
        ("(clicks)", "The rounded reporter - drop it into any slot to use the value the box is holding."),
        ("join () ()", "A green Operator that sticks two things together, like \\emph{Clicks:} and the number."),
    ],
    steps=[
        "Make a \\blk{when green flag clicked} script with one block: "
        "\\blk{set [clicks] to (0)}. This resets the count each time you start.",
        "Make a second script: \\blk{when this sprite clicked}.",
        "Under it add \\blk{change [clicks] by (1)}.",
        "Then add \\blk{say (join (Clicks: ) (clicks))}. Drag the \\blk{join} "
        "Operator into the say slot, type \\emph{Clicks: } in its left box, and "
        "drop the \\blk{clicks} reporter into its right box.",
        "Click the green flag, then click the cat a few times. The number climbs "
        "and the cat reads it out.",
    ],
    script_intro="Two scripts: reset on the flag (left), count on each click (right):",
    scripts=[
        script(when_flag(), set_var("clicks", 0), caption="Green flag: reset"),
        script(
            when_clicked(),
            change_var("clicks", 1),
            say(join("Clicks: ", var("clicks"))),
            caption="Click: count up",
        ),
    ],
    note="The box on the stage and the \\blk{clicks} reporter are the same "
         "variable. Change it in one place and both update - the program is "
         "remembering one number for you.",
    tasks=[
        ("Add a reset key: make a \\blk{when [r] key pressed} script with "
         "\\blk{set [clicks] to (0)}.", "Pressing r sets the count back to zero."),
        ("Celebrate a milestone: in the click script, after the change, add "
         "\\blk{if <(clicks) = (10)>} then \\blk{say (Ten! You win.) for (2) "
         "seconds}.", "At exactly 10 clicks the cat shouts Ten! You win."),
        ("Grow with the count: also add \\blk{change size by (5)} in the click "
         "script so the cat gets bigger every click.",
         "The cat grows a little each time, alongside the rising number."),
    ],
)


# ---- Project 2: pick random + score - whack-a-cat ----------------------------

p2 = BUILD(
    "Whack-a-cat",
    goal="The cat pops up at a random spot, waits a moment, then jumps somewhere "
         "new. Click it before it moves to score a point. A \\blk{score} variable "
         "keeps your total, and \\blk{pick random} makes every round different.",
    setup="Make a variable called \\textbf{score} (Variables group, Make a "
          "Variable).",
    new_blocks=[
        ("pick random () to ()", "A green Operator. It gives a fresh random number in the range each time it runs."),
        ("go to x: () y: ()", "Jump to a spot - here the x and y are random, so the cat appears anywhere."),
    ],
    steps=[
        "Start with \\blk{when green flag clicked}, then \\blk{set [score] to (0)}.",
        "Add a \\blk{forever} loop.",
        "Inside it, add \\blk{go to x: (pick random (-200) to (200)) y: (pick "
        "random (-150) to (150))}. Drop a \\blk{pick random} Operator into each "
        "of the x and y slots.",
        "Under that, still inside the loop, add \\blk{wait (1) seconds}.",
        "Make a second script: \\blk{when this sprite clicked}, then "
        "\\blk{change [score] by (1)} and \\blk{start sound [Pop]}.",
        "Green flag. The cat hops around - click it quickly to run up the score.",
    ],
    script_intro="The hopping loop (left) and the score-on-click script (right):",
    scripts=[
        script(
            when_flag(),
            set_var("score", 0),
            forever(
                goto_xy(pick_random(-200, 200), pick_random(-150, 150)),
                wait(1),
            ),
            caption="Hop to a random spot",
        ),
        script(
            when_clicked(),
            change_var("score", 1),
            play_sound("Pop"),
            caption="Click: +1 point",
        ),
    ],
    note="\\blk{pick random (1) to (6)} is like rolling a die: a new number every "
         "time. That is what keeps the game from being the same twice.",
    tasks=[
        ("Make it harder: change \\blk{wait (1) seconds} to \\blk{wait (0.6) "
         "seconds} so the cat does not sit still as long.",
         "The cat moves sooner, leaving less time to click."),
        ("Read the score aloud: in the click script add \\blk{say (join (Score: ) "
         "(score)) for (0.5) seconds}.", "The cat announces the running score on each hit."),
        ("Vary the timing: change \\blk{wait (1) seconds} to \\blk{wait (pick "
         "random (0.4) to (1.2)) seconds} so the pause is unpredictable.",
         "Each hop waits a random amount, so the rhythm keeps changing."),
    ],
)


# ---- Project 3: ask / answer + repeat until - guess my number ---------------

p3 = BUILD(
    "Guess my number",
    goal="The computer thinks of a secret number from 1 to 10 and you try to "
         "guess it. After each guess it says higher or lower, and it keeps asking "
         "until you are right. This is a loop with a finish line: \\blk{repeat "
         "until} the guess matches.",
    setup="Make a variable called \\textbf{secret}.",
    new_blocks=[
        ("ask () and wait", "A Sensing block. It shows a question and a text box, and waits for the player to type."),
        ("(answer)", "A Sensing reporter holding whatever the player just typed."),
        ("repeat until <>", "A Control loop. It runs its blocks over and over until the hexagon question becomes true."),
        ("() > () and () = ()", "Green Operator comparisons. Each is true or false, so each fits an if or a loop."),
    ],
    steps=[
        "Start with \\blk{when green flag clicked}.",
        "Add \\blk{set [secret] to (pick random (1) to (10))} so the computer "
        "picks a hidden number.",
        "Add \\blk{ask (I picked 1-10. Guess?) and wait}.",
        "Drag in \\blk{repeat until <(answer) = (secret)>}. Build the hexagon "
        "with the green \\blk{() = ()} Operator, the \\blk{answer} reporter, and "
        "the \\blk{secret} reporter.",
        "Inside the loop add an \\blk{if <> then ... else ...}. Put \\blk{(answer) "
        "$>$ (secret)} in its hexagon, \\blk{say (Too big!) for (1) seconds} in "
        "the if part, and \\blk{say (Too small!) for (1) seconds} in the else "
        "part. Then add \\blk{ask (Guess again) and wait} so the player tries again.",
        "After the loop add \\blk{say (You got it!) for (2) seconds}.",
        "Green flag, and play. The cat guides you in until you land on the secret.",
    ],
    scripts=script(
        when_flag(),
        set_var("secret", pick_random(1, 10)),
        ask("I picked 1-10. Guess?"),
        repeat_until(eq(answer(), var("secret")),
                     ifelse(gt(answer(), var("secret")),
                            [say_for("Too big!", 1)],
                            [say_for("Too small!", 1)]),
                     ask("Guess again")),
        say_for("You got it!", 2),
    ),
    note="\\blk{repeat until} checks its question before each pass. The moment "
         "your guess equals the secret, the loop stops and the cat congratulates "
         "you.",
    tasks=[
        ("Count the guesses: make a variable \\blk{guesses}, \\blk{set [guesses] "
         "to (0)} after the flag, and \\blk{change [guesses] by (1)} inside the "
         "loop. End with \\blk{say (join (Guesses: ) (guesses)) for (2) seconds}.",
         "The cat reports how many tries it took."),
        ("Make it harder: change \\blk{pick random (1) to (10)} to \\blk{(1) to "
         "(100)} and update the question text.",
         "A wider range means more guesses to home in."),
        ("Reveal the answer: change the ending to \\blk{say (join (It was ) "
         "(secret)) for (2) seconds}.", "The cat shows the secret number it had chosen."),
    ],
)


# ---- Project 4: capstone - catch the falling apple ---------------------------

p4 = BUILD(
    "Mini project: catch the apple",
    goal="A real score game. An apple falls from the top at a random spot; steer "
         "the cat to catch it and your \\blk{score} goes up. Miss it and it "
         "starts again from the top. Everything from this sheet, working together.",
    setup="Steer the cat with the four arrow-key scripts from \\emph{Scratch A} "
          "(Project 2). Then add an \\textbf{Apple} sprite: click \\emph{Choose "
          "a Sprite} (bottom right) and pick Apple. Make a variable "
          "\\textbf{score} \\emph{For all sprites}. The script below goes on the "
          "\\textbf{Apple}.",
    new_blocks=[
        ("touching [Sprite1]?", "A Sensing hexagon, true when the apple touches the cat (the cat sprite is named Sprite1)."),
        ("change y by ()", "Move up or down. A negative number makes the apple fall."),
    ],
    steps=[
        "On the Apple, start with \\blk{when green flag clicked}, then "
        "\\blk{set [score] to (0)}.",
        "Add \\blk{go to x: (pick random (-220) to (220)) y: (160)} so the apple "
        "starts at the top in a random column.",
        "Add a \\blk{forever} loop. Inside, add \\blk{change y by (-5)} so the "
        "apple falls.",
        "Still in the loop, add \\blk{if <touching [Sprite1]?>} then "
        "\\blk{change [score] by (1)}, \\blk{start sound [Chomp]}, and "
        "\\blk{go to x: (pick random (-220) to (220)) y: (160)} - caught, so "
        "score and respawn at the top.",
        "Add one more \\blk{if <touching [edge]?>} then \\blk{go to x: (pick "
        "random (-220) to (220)) y: (160)} so a missed apple restarts from the "
        "top when it hits the floor.",
        "Green flag. Catch falling apples with the arrow keys and watch the "
        "score climb.",
    ],
    script_intro="The Apple's script (the cat uses the Scratch A arrow keys):",
    scripts=script(
        when_flag(),
        set_var("score", 0),
        goto_xy(pick_random(-220, 220), 160),
        forever(
            changey(-5),
            if_(touching("Sprite1"),
                change_var("score", 1),
                play_sound("Chomp"),
                goto_xy(pick_random(-220, 220), 160)),
            if_(touching("edge"),
                goto_xy(pick_random(-220, 220), 160)),
        ),
    ),
    note="The apple only moves up and down within the random columns, so the only "
         "edge it ever reaches is the floor - that is how \\blk{touching [edge]?} "
         "spots a miss.",
    tasks=[
        ("Add lives: make a variable \\blk{lives}, \\blk{set [lives] to (3)} after "
         "the flag. In the \\blk{touching [edge]?} part add \\blk{change [lives] "
         "by (-1)}, then \\blk{if <(lives) = (0)>} then \\blk{say (Game Over) for "
         "(2) seconds} and \\blk{stop [all]}.",
         "A missed apple costs a life; at zero lives the game stops."),
        ("Speed it up: change \\blk{change y by (-5)} to \\blk{change y by (-8)} "
         "so the apples fall faster.", "Faster apples are harder to catch."),
        ("Add a second apple: right-click the Apple sprite and choose "
         "\\emph{duplicate}. The copy runs the same script on its own.",
         "Two apples fall at once, doubling the action."),
    ],
)


ACTIVITIES = [p1, p2, p3, p4]
