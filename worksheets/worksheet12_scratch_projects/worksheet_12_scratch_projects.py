"""Building-Scratch-Projects Worksheet - a follow-along first taste of Scratch.

The class has met the coordinate stage (Worksheet 11) and read Scratch scripts
on paper. Now they open Scratch and BUILD. Each project is a tiny, finished thing
they make at the computer; the sheet shows the exact blocks to snap together (the
single source, rendered via the scratch3 package) so the picture matches the prose.

The ramp is: basic blocks, then events (keys, clicks), then a forever loop, then
a capstone that combines them.

  Project 1  sequence + green flag   a script that runs top to bottom
  Project 2  events: arrow keys      four little when-key scripts that steer
  Project 3  control: forever        the cat walks by itself, animated
  Project 4  events: sprite clicked  click the cat and it reacts
  Project 5  capstone                flag-reset + steering + a click, together

The language is kept simple and short for first-time programmers, and every block
name matches the wording Scratch shows.
"""

from gens.scratchgen import (
    BUILD, script,
    when_flag, when_key, when_clicked,
    move, point, goto_xy, changex, changey, bounce, set_rotation_style,
    say_for, next_costume, set_size,
    play_sound, wait, forever,
)

TITLE = "Scratch A"

# ---- Project 1: a first script - runs top to bottom --------------------------

p1 = BUILD(
    "Your first script",
    goal="Click the green flag. The cat says hello and slides across the stage. "
         "This is a program: blocks that run one by one, from top to bottom.",
    setup="Open a new Scratch project. The cat is already on the stage.",
    new_blocks=[
        ("when green flag clicked", "A yellow Events block. It starts the script when you click the green flag."),
        ("go to x: () y: ()", "Jump to a spot on the stage. The middle is x: 0, y: 0."),
        ("say () for () seconds", "Show a speech bubble for a short time."),
        ("move () steps", "Slide forward by a number of steps."),
    ],
    steps=[
        "From the yellow Events blocks, drag out \\blk{when green flag clicked}. "
        "Every script starts with a block like this on top.",
        "From the blue Motion blocks, join \\blk{go to x: -150 y: 0} under it. Now "
        "the cat always starts on the left.",
        "From the purple Looks blocks, add \\blk{say (Hi! Watch me move.) for (1) "
        "seconds}.",
        "Add \\blk{move (200) steps} from the Motion blocks.",
        "Click the green flag above the stage. The cat says hello, then slides to "
        "the right.",
    ],
    scripts=script(
        when_flag(),
        goto_xy(-150, 0),
        say_for("Hi! Watch me move.", 1),
        move(200),
    ),
    tasks=[
        ("Change the words in the \\blk{say} block to your own greeting.", ""),
        ("Add one more \\blk{say} block at the very end, so the cat says something "
         "after it stops moving.", "Join another say block under move (200) steps."),
        ("Make the cat reach the right edge: change \\blk{move (200) steps} to a "
         "bigger number, like 300.", "About 330 steps reaches the right edge from x: -150."),
    ],
)

# ---- Project 2: events - steer the cat with the arrow keys -------------------

p2 = BUILD(
    "Move with the arrow keys",
    goal="Make the cat move when you press an arrow key. Each key gets its own "
         "small script. A script runs only when you press its key.",
    new_blocks=[
        ("when [space] key pressed", "A yellow Events block. It runs when you press the key you pick."),
        ("change x by ()", "Move across the stage. Right is a plus number. Left is a minus number."),
        ("change y by ()", "Move up or down. Up is a plus number. Down is a minus number."),
    ],
    steps=[
        "Drag out \\blk{when [space] key pressed}. Click the small arrow on the "
        "block and pick \\textbf{right arrow}.",
        "Join \\blk{change x by (10)} under it. Press the right arrow key. The cat "
        "moves right.",
        "Make three more in the same way: \\textbf{left arrow} with "
        "\\blk{change x by (-10)}, \\textbf{up arrow} with \\blk{change y by (10)}, "
        "and \\textbf{down arrow} with \\blk{change y by (-10)}.",
        "Now you have four small scripts. Press the arrow keys to move the cat "
        "around.",
    ],
    note="Think back to the stage grid. x is how far across. y is how far up. That "
         "is why right and up use plus numbers, and left and down use minus numbers.",
    scripts=[
        script(when_key("right arrow"), changex(10),  caption="Move right"),
        script(when_key("left arrow"),  changex(-10), caption="Move left"),
        script(when_key("up arrow"),    changey(10),  caption="Move up"),
        script(when_key("down arrow"),  changey(-10), caption="Move down"),
    ],
    tasks=[
        ("Make the cat move faster: change every 10 to 20, and every -10 to -20.",
         "Bigger numbers move the cat further on each press."),
        ("Add \\blk{point in direction (90)} to the right script and "
         "\\blk{point in direction (-90)} to the left script, so the cat faces the "
         "way it moves.", "The cat turns to face right or left as it walks."),
    ],
)

# ---- Project 3: control - the forever loop animates a walk -------------------

p3 = BUILD(
    "Make it walk on its own",
    goal="Use a forever loop. The cat walks across the stage on its own. It moves, "
         "swaps its legs, and turns around at the edges. You do not press any key.",
    new_blocks=[
        ("forever", "An orange Control loop. It runs the blocks inside it again and again, without stopping."),
        ("next costume", "Swap to the cat's other picture. Doing this fast makes it look like it is walking."),
        ("if on edge, bounce", "Turn around when the cat reaches the side of the stage."),
        ("wait () seconds", "Pause before the next block. This sets the speed."),
    ],
    steps=[
        "Start a new script with \\blk{when green flag clicked}.",
        "Add \\blk{set rotation style [left-right]}. This stops the cat from "
        "turning upside down when it turns around.",
        "From the orange Control blocks, drag in \\blk{forever}. It is a C shape. "
        "The blocks you put inside it run again and again.",
        "Inside the forever, put these blocks in order: \\blk{move (10) steps}, "
        "\\blk{if on edge, bounce}, \\blk{next costume}, \\blk{wait (0.2) seconds}.",
        "Click the green flag. The cat walks back and forth on its own.",
    ],
    scripts=script(
        when_flag(),
        set_rotation_style("left-right"),
        forever(
            move(10),
            bounce(),
            next_costume(),
            wait(0.2),
        ),
    ),
    note="A forever loop never stops on its own. Click the red stop sign above the "
         "stage to stop it.",
    tasks=[
        ("Change the \\blk{wait (0.2) seconds} time so the cat walks at a speed you "
         "like.", "A smaller wait is faster. Try 0.05 and 0.5."),
        ("Before the \\blk{forever} loop, add \\blk{go to x: -200 y: -120} so the "
         "cat always starts at the bottom-left.", "The cat begins each run in the same corner."),
        ("Also before the loop, add \\blk{set size to (70) \\%} so the cat is a bit "
         "smaller as it walks.", "The cat starts at 70 percent size, then walks."),
    ],
)

# ---- Project 4: events - click the sprite to react ---------------------------

p4 = BUILD(
    "Click the cat",
    goal="Try a new kind of event. This time the cat does something when you click "
         "it, not when you press a key. When you click it, the cat meows and "
         "changes its pose.",
    new_blocks=[
        ("when this sprite clicked", "A yellow Events block. It runs when you click the sprite on the stage."),
        ("start sound [Meow]", "Play the cat's meow sound."),
        ("change size by ()", "Make the sprite bigger with a plus number, or smaller with a minus number."),
    ],
    steps=[
        "Drag out \\blk{when this sprite clicked}.",
        "From the pink Sound blocks, add \\blk{start sound [Meow]}.",
        "From the Looks blocks, add \\blk{say (Meow!) for (1) seconds}, then "
        "\\blk{next costume}.",
        "Click the cat on the stage. It meows, talks, and changes its pose.",
    ],
    scripts=script(
        when_clicked(),
        play_sound("Meow"),
        say_for("Meow!", 1),
        next_costume(),
    ),
    tasks=[
        ("Add \\blk{change size by (10)} at the end, so the cat grows a little each "
         "time you click it.", "Each click adds 10 to the size."),
        ("After that, add \\blk{wait (1) seconds} then \\blk{change size by (-10)}, "
         "so the cat grows, waits, then goes back to its size.",
         "It grows, pauses, then shrinks back by the same amount."),
        ("Swap \\blk{start sound [Meow]} for a different sound. Click the Sounds "
         "tab at the top left to pick one.", "Any sound from the Sounds tab works."),
    ],
)

# ---- Project 5: capstone - put the events together ---------------------------

p5 = BUILD(
    "Mini project: put it all together",
    goal="Put your blocks together into one small project. The green flag puts the "
         "cat back in the middle and tells the player what to do. The arrow keys "
         "move it. Clicking it makes it cheer.",
    setup="Keep your four arrow-key scripts from Project 2. This project uses them "
          "again. You will add the two scripts below.",
    steps=[
        "Add a \\blk{when green flag clicked} script that sets up the cat: "
        "\\blk{go to x: 0 y: 0}, \\blk{point in direction 90}, "
        "\\blk{set size to (100) \\%}, then \\blk{say (Use the arrows to move me!) "
        "for (2) seconds}.",
        "Add a \\blk{when this sprite clicked} script that makes the cat cheer: "
        "\\blk{say (Yay!) for (1) seconds}, then \\blk{next costume}.",
        "Click the green flag. Move the cat with the arrow keys, and click it to "
        "make it cheer. You have built a small project you can play!",
    ],
    script_intro="Your two new scripts (the four arrow-key scripts from Project 2 "
                 "run with these):",
    scripts=[
        script(
            when_flag(),
            goto_xy(0, 0),
            point(90),
            set_size(100),
            say_for("Use the arrows to move me!", 2),
            caption="Green flag: set up and explain",
        ),
        script(
            when_clicked(),
            say_for("Yay!", 1),
            next_costume(),
            caption="Click: cheer",
        ),
    ],
    tasks=[
        ("Give the cat a backdrop. Click \\emph{Stage} at the bottom right, then "
         "\\emph{Choose a Backdrop}.", ""),
        ("Change the green-flag \\blk{say} block to your own instructions for the "
         "player.", ""),
        ("Add one more \\blk{when green flag clicked} script with a \\blk{forever} "
         "loop that spins the cat slowly: \\blk{turn (3) degrees}, then "
         "\\blk{wait (0.1) seconds}.",
         "The forever loop turns the cat a little, waits, and repeats, so it spins."),
    ],
)

ACTIVITIES = [p1, p2, p3, p4, p5]
