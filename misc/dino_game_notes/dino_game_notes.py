"""Dino Run - teaching notes: the moving ground, the cactus, score, and game over.

Not a numbered worksheet - a stand-alone set of build-along notes for the Chrome
Dino game, written with the same scratchgen infra as the Scratch E/F capstones so
the blocks the student matches are exactly the scripts the prose describes.

Scope is the four pieces asked for, in build order:

  1  Moving ground     two 480-wide tiles leapfrogging -> an endless belt
  2  The cactus        the falling rock of Scratch F, turned on its side
  3  Score & game over survive to score; touch a cactus and it is over

The star is the ground. The rest is Rock Dodge (Scratch F) rotated 90 degrees:
the rock fell down and reset to the top; the cactus runs left and resets to the
right. Same idea, sideways. An interactive picture of the ground leapfrog lives
at cs17.org/ground-leapfrog-visualizer.html.
"""

import os

from gens.scratchgen import (
    BUILD, script, gap,
    when_flag, when_key, when_clone, when_receive,
    goto_xy, glide, changex, x_position,
    show, hide, set_size,
    forever, repeat_until, if_, wait, stop_all,
    create_clone, delete_clone, broadcast,
    say, say_for, set_var, change_var, var, join,
    touching, lt, pick_random,
)

# Real Chrome-Dino costumes (the sliced PNGs) live in scratch-dino/assets/sliced.
# This is a teacher-reference sheet, so the figures use the actual sprites, small,
# instead of abstract markers.
_ASSETS = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..",
                 "scratch-dino", "assets", "sliced"))


def _sprite(x, y, name, dim, anchor="south") -> str:
    return (r"\node[anchor=%s,inner sep=0] at (%.2f,%.2f) "
            r"{\includegraphics[%s]{%s/%s}};"
            % (anchor, x, y, dim, _ASSETS, name))


def mockup() -> str:
    """A real-sprite mock-up of the finished game: Dino + cactuses on the moving
    ground, clouds drifting above, the score readout - built from the actual
    sliced costumes so the teacher sees exactly what it should look like."""
    parts = [
        r"\par\vspace{8pt}\begin{center}\fbox{\begin{minipage}{0.86\linewidth}"
        r"\centering\vspace{4pt}\textbf{\footnotesize What you are building}"
        r"\par\vspace{6pt}\begin{tikzpicture}[x=1cm,y=1cm]",
        r"\fill[blue!4,rounded corners=3pt] (0,0) rectangle (9,4.2);",
        r"\draw[gray!45,rounded corners=3pt,line width=0.7pt] (0,0) rectangle (9,4.2);",
        _sprite(4.5, 1.02, "ground.png", "width=8.8cm"),
        r"\draw[brown!45,line width=0.5pt] (0.1,1.04) -- (8.9,1.04);",
        _sprite(2.4, 3.35, "cloud.png", "height=0.5cm", anchor="center"),
        _sprite(6.2, 3.62, "cloud.png", "height=0.42cm", anchor="center"),
        _sprite(1.4, 1.04, "dino_run_1.png", "height=1.0cm"),
        _sprite(3.7, 1.04, "cactus_small_1.png", "height=0.62cm"),
        _sprite(5.4, 1.04, "cactus_large_1.png", "height=0.86cm"),
        _sprite(7.4, 1.04, "cactus_small_2.png", "height=0.58cm"),
        r"\node[anchor=north east,font=\ttfamily\scriptsize,text=gray!60] "
        r"at (8.8,4.0) {score 0};",
        r"\draw[->,gray!55,line width=0.5pt,>=Stealth] (7.9,2.0) -- (6.9,2.0);",
        r"\node[font=\tiny,text=gray!70,anchor=south] at (7.4,2.05) {rush left};",
        r"\draw[->,gray!45,line width=0.4pt,>=Stealth] (6.65,3.4) -- (6.1,3.4);",
        r"\node[font=\tiny,text=gray!60,anchor=south] at (6.35,3.45) {drift};",
        r"\end{tikzpicture}\par\vspace{5pt}\footnotesize\itshape The finished game: "
        r"the Dino runs in place while the ground and cactuses rush left, clouds "
        r"drift slowly above (parallax), and the score climbs until a cactus catches "
        r"you.\vspace{3pt}\end{minipage}}\end{center}",
    ]
    return "".join(parts)

TITLE = "Dino Run - Ground, Cactus, Score \\& Game Over"

PALETTE = ["Motion", "Looks", "Sound", "Events", "Control",
           "Sensing", "Operators", "Variables"]

LEAD = (
    r"\textbf{Dino Run - teacher reference.}\quad Building on a Dino that already "
    r"runs (swapping costumes) and jumps in place, these notes carry the game to "
    r"the finish in five pieces, each a small project with its complete scripts: a "
    r"\emph{moving ground} so the world rushes past, drifting \emph{clouds} for "
    r"depth, \emph{cactuses} to jump over, a \emph{score} that climbs while you "
    r"survive, and finally a \emph{broadcast} that ends the game on a crash. The "
    r"order is deliberate - each piece sets up the next, and the score piece stops "
    r"at a wall (a crash it cannot act on) that the broadcast piece knocks down. "
    r"The endless ground is the one genuinely new trick, so it goes first; watch it "
    r"move at \texttt{cs17.org/ground-leapfrog-visualizer.html}. Every script below "
    r"is shown finished - assemble in the real Dino project on "
    r"\texttt{scratch.mit.edu}."
    + mockup())


# ---- Project 1: the moving ground --------------------------------------------

p1 = BUILD(
    "The moving ground",
    goal="Make the ground rush past forever. The trick: two ground tiles, each a "
         "little wider than the stage, chasing each other left. When one slides a "
         "full stage-width off the left, it leaps back to the right behind its "
         "partner - and because the tiles are a touch wider than the screen, they "
         "overlap, so there is never a gap. That endless belt is what makes the "
         "Dino feel like it is running.",
    setup="Draw or import a ground strip a little \\textbf{wider than the stage} - "
          "make it \\textbf{520 wide} (the stage is 480) - and name the sprite "
          "\\textbf{Ground1}. It sits low, at y: -80. The extra 40 pixels are what "
          "let the two tiles overlap and hide the seam (see the note). You build "
          "Ground1's script, then duplicate it into Ground2.",
    new_blocks=[
        ("x position", "A blue Motion reporter: how far left or right the sprite's centre is. Near the right edge it is a big plus number; as the tile slides left it drops past -240 into the minuses."),
        ("if <(x position) $<$ (-480)>", "True once this tile has slid a full stage-width left - its partner now covers the whole screen, so this tile is free to leap."),
        ("change x by (960)", "Leap the tile two stage-widths to the right, landing it just behind its partner and keeping the pair 480 apart."),
    ],
    steps=[
        "On \\textbf{Ground1}, start with \\blk{when green flag clicked}, then "
        "\\blk{go to x: 0 y: -80}. This tile fills the stage (and a touch more - it "
        "is 520 wide).",
        "Add a \\blk{forever} loop. Its first block is given: \\blk{change x by "
        "(-6)}, which slides the tile left a little every tick.",
        "Below it is an \\blk{if} shell with two \\blk{? your turn} gaps. The grey "
        "hexagon is the test: has this tile slid a \\emph{full stage-width} off the "
        "left? The grey block inside is the action: leap it back to the right, "
        "behind its partner.",
        "Green flag. One tile scrolls left and leaves a blank gap behind it - that "
        "is expected, one tile cannot cover the screen and be sliding off at once. "
        "We need a second tile to fill that gap.",
        "Right-click Ground1 and choose \\emph{duplicate}. Rename the copy "
        "\\textbf{Ground2}. Change \\emph{only} its start block to \\blk{go to x: "
        "480 y: -80} - everything else stays identical. Now while Ground1 fills the "
        "screen, Ground2 waits just off the right; they take turns forever, "
        "overlapping by 40 pixels so no seam ever shows.",
    ],
    script_intro="Ground1's scroll loop. Fill the two grey gaps in the \\blk{if} - "
                 "the test (grey hexagon) and the leap (grey block). Ground2 is "
                 "this exact script with a start of x: 480:",
    scripts=script(
        when_flag(),
        goto_xy(0, -80),
        forever(
            changex(-6),
            if_(gap("has this tile slid a full stage-width off the left?",
                    lt(x_position(), -480)),
                gap("leap it two stage-widths right, behind its partner",
                    changex(960))),
        ),
        caption="Ground1: scroll left, then leap (Ground2 = same, start x: 480)",
    ),
    note="Why 520 wide and not exactly 480? Because \\textbf{Scratch fences every "
         "sprite} - it never lets a sprite slide fully off the stage, always "
         "keeping about 15 pixels on screen. An exactly-480 tile's centre can "
         "therefore never reach -480, so \\blk{if <(x position) $<$ (-480)>} would "
         "never be true and the belt would jam. Widening each tile to 520 fixes "
         "both halves: the wider box may legally slide until its centre passes -480 "
         "(so the test fires), and the 40-pixel overlap covers the hand-off - when "
         "a tile passes -480 its partner is already at x: 0 covering the screen, so "
         "the leap is invisible."
         "\\par\\vspace{4pt}{\\normalfont\\small \\textbf{Why \\texttt{change x by "
         "(960)} and not \\texttt{set x to (480)}?} Both put the tile back on the "
         "right, but only \\texttt{change x} carries the fence overshoot forward, "
         "so the two tiles keep more overlap at every speed. One wrap at speed -50 "
         "- the step overshoots to -500 and the fence clamps it to -485:"
         "\\par\\vspace{3pt}\\begin{center}\\fbox{\\begin{minipage}{0.9\\linewidth}"
         "\\centering\\small\\renewcommand{\\arraystretch}{1.2}"
         "\\begin{tabular}{@{}c l r l l@{}}"
         "tick & G1 (raw$\\to$fenced) & G2 & \\texttt{change x}$\\to$G1 (ovl) & "
         "\\texttt{set x}$\\to$G1 (ovl)\\\\\\hline "
         "9 & $-450$ & $30$ & $-450$ & $-450$\\\\ "
         "\\textbf{10} & $-500\\to\\mathbf{-485}$ & $-20$ & $\\mathbf{475}$\\ (25) & "
         "$\\mathbf{480}$\\ (20)\\\\ "
         "11 & --- & $-70$ & $425$\\ (25) & $430$\\ (20)\\\\ "
         "12 & --- & $-120$ & $375$\\ (25) & $380$\\ (20)\\\\ "
         "\\end{tabular}\\par\\vspace{3pt}\\footnotesize overlap $=520-(\\mathrm{G1}"
         "-\\mathrm{G2})$; a gap opens only if it drops below 0. Here \\emph{both} "
         "stay safe - the 40-pixel cushion absorbs the drift - but \\texttt{change "
         "x} keeps more: it carries the fence overshoot forward, \\texttt{set x} "
         "throws it away. Prefer \\texttt{change x by (960)} because it needs no "
         "fixed 480 and keeps working with more tiles, other widths, or a changing "
         "speed - not because \\texttt{set x} visibly tears here (it does not, until "
         "very high speeds, and then both do)."
         "\\end{minipage}}\\end{center}} "
         "Watch it at \\texttt{cs17.org/ground-leapfrog-visualizer.html}.",
    tasks=[
        ("Change both tiles' \\blk{change x by (-6)} together to set the running "
         "speed. Bigger negative = faster world.",
         "The ground rushes past faster, so the game feels quicker."),
        ("Make one \\blk{speed} variable (For all sprites), \\blk{set [speed] to "
         "(6)} once, and use \\blk{change x by ((0) - (speed))} on both tiles. "
         "Later the cactus can read the same variable so ground and cactus always "
         "match.", "One number controls how fast the whole world moves."),
        ("Add depth: a second, faraway backdrop layer (hills, clouds) on its own "
         "pair of tiles scrolling slower, say \\blk{-3}. Near things move faster "
         "than far things - that is parallax.",
         "The background drifts slowly behind the fast ground, giving a sense of "
         "distance."),
    ],
)


# ---- Project 2: clouds (the first clones) ------------------------------------

p_cloud = BUILD(
    "Clouds drifting by (your first clones)",
    goal="Fill the sky with clouds that drift slowly past, far behind the action. "
         "This is your first taste of \\emph{clones}: the Cloud sprite stays hidden "
         "and spawns copies of itself; each copy drifts across on its own and then "
         "deletes itself. No jumping, no score - clouds are just scenery, so it is "
         "the gentlest way to meet clones. The one trick that sells the depth: "
         "clouds move much \\emph{slower} than the ground.",
    setup="Add a \\textbf{Cloud} sprite (\\emph{Choose a Sprite}, or paint a small "
          "puffy cloud) and name it \\textbf{Cloud}. It gets two scripts: one that "
          "spawns clones, and one that each clone runs. Clouds never touch the "
          "Dino, so there is no collision to worry about.",
    new_blocks=[
        ("create clone of [myself]", "Make a live copy of this sprite. Each copy runs its own \\blk{when I start as a clone} script from the top."),
        ("when I start as a clone", "A hat: the script under it runs on each new clone the instant it is born."),
        ("delete this clone", "Remove this clone once it has drifted off screen, so clones do not pile up."),
        ("pick random (2) to (5)", "An Operators reporter: a fresh random number each time - here the gap in seconds between clouds, so they never come evenly."),
    ],
    steps=[
        "First the \\textbf{spawner}. On \\textbf{Cloud}: \\blk{when green flag "
        "clicked}, then \\blk{hide} - the original never shows, it only makes "
        "clones. Add a \\blk{forever} whose first block is \\blk{wait (pick random "
        "(2) to (5)) seconds} (the random gap between clouds).",
        "The next block is a \\blk{? your turn}: make a new cloud. (Which Control "
        "block creates a copy of this sprite?)",
        "Now the \\textbf{clone} script. Start it with \\blk{when I start as a "
        "clone}, then \\blk{set size to (70) \\%} (clouds are small - they are far "
        "away), \\blk{go to x: (240) y: (pick random (60) to (150))} (the right "
        "edge, at a random height up in the sky), and \\blk{show}.",
        "Add a \\blk{repeat until} loop holding \\blk{change x by (-1)} - a slow "
        "drift, much slower than the ground's -6. The \\blk{? your turn} is the "
        "grey hexagon: stop once the cloud has drifted off the left edge.",
        "After the loop, \\blk{delete this clone} is given. Green flag: clouds "
        "drift in from the right at random heights and gaps, slow and silent behind "
        "everything else.",
    ],
    script_intro="The spawner, then the clone's drift loop. Fill the grey block "
                 "(make a clone) and the grey hexagon (the off-left test):",
    stack=True,
    scripts=[
        script(
            when_flag(),
            hide(),
            forever(
                wait(pick_random(2, 5)),
                gap("make a new cloud", create_clone()),
            ),
            caption="Cloud (original): stay hidden, spawn a cloud now and then",
        ),
        script(
            when_clone(),
            set_size(70),
            goto_xy(240, pick_random(60, 150)),
            show(),
            repeat_until(
                gap("has this cloud drifted off the left edge?",
                    lt(x_position(), -240)),
                changex(-1)),
            delete_clone(),
            caption="Each cloud: drift slowly in from the right, then delete off the left",
        ),
    ],
    note="This is exactly the pattern the cactus will use next - a hidden "
         "\\emph{spawner} making clones, each running the same short script and then "
         "cleaning itself up with \\blk{delete this clone}. Clouds are the easy "
         "version: they cannot hurt you, so there is no \\blk{touching} test and no "
         "score - just drift and delete. The slow \\blk{change x by (-1)} is the "
         "whole point: the real Chrome game moves clouds at about a \\emph{fifth} of "
         "the ground speed, so near things (ground, cactus) rush by while far things "
         "(clouds) creep - that difference is called \\textbf{parallax}, and it is "
         "what makes a flat screen feel deep.",
    tasks=[
        ("Vary the size: change \\blk{set size to (70)} to \\blk{set size to (pick "
         "random (40) to (80))} so some clouds look nearer (bigger) and some "
         "farther (smaller).", "Clouds come in different sizes, adding depth."),
        ("Give each cloud its own drift speed: at the top of the clone script pick "
         "a number into a \\blk{my drift} variable and use \\blk{change x by ((0) - "
         "(my drift))}, so some clouds crawl and some glide.",
         "The sky feels alive - clouds move at their own paces."),
        ("Tie clouds to the game speed: use \\blk{change x by ((0) - (speed) / (5))} "
         "so when the game speeds up the clouds do too - but always a fifth as "
         "fast, just like Chrome.",
         "The whole world speeds up together, keeping the depth."),
    ],
)


# ---- Project 3: the cactus (clones again, now on the ground) ------------------

p2 = BUILD(
    "The cactuses",
    goal="Send cactuses charging in from the right, two or three on screen at "
         "once, at random gaps - so the run never feels the same twice. It uses the "
         "same \\emph{clone} trick you just met with the clouds - a hidden sprite "
         "spawning copies that each run across and delete themselves - but now the "
         "copies sit on the \\emph{ground} and race at \\emph{full speed}, because "
         "you have to jump them.",
    setup="Add a \\textbf{Cactus} sprite (\\emph{Choose a Sprite}: a cactus, a "
          "ball, anything spiky), make it small, and name it \\textbf{Cactus}. "
          "You will give it two scripts: one that spawns clones, and one that "
          "each clone runs.",
    new_blocks=[
        ("create clone of [myself]", "Same as the clouds: make a live copy that runs its own \\blk{when I start as a clone} script."),
        ("when I start as a clone", "Same hat as the clouds - runs on each new cactus clone the instant it is born."),
        ("delete this clone", "Same as the clouds: remove the clone once it has done its job."),
        ("repeat until <(x position) $<$ (-250)>", "Keep the clone moving left until it has passed the left edge (x: -240); then stop and delete it."),
    ],
    steps=[
        "First the \\textbf{spawner}. On \\textbf{Cactus}: \\blk{when green flag "
        "clicked}, then \\blk{hide} - the original never shows, it only makes "
        "clones. Add a \\blk{forever} whose first block is \\blk{wait (pick random "
        "(0.8) to (2)) seconds} (the random gap between cactuses).",
        "The next block is a \\blk{? your turn}: make a new cactus. (Which Control "
        "block creates a copy of this sprite?)",
        "Now the \\textbf{clone} script. Start it with \\blk{when I start as a "
        "clone}, then \\blk{set size to (50) \\%}, \\blk{go to x: (240) y: -55} "
        "(the right edge, on the ground), and \\blk{show}.",
        "Add a \\blk{repeat until} loop holding \\blk{change x by (-6)} - the same "
        "speed as the ground. The \\blk{? your turn} is the grey hexagon: stop "
        "when the cactus has run off the left edge.",
        "After the loop, \\blk{delete this clone} is given - the cactus is gone, "
        "so remove the copy.",
        "Green flag. Cactuses stream in from the right, two or three at a time, at "
        "changing gaps. Jump them!",
    ],
    script_intro="The spawner, then the clone's run loop. Fill the grey block "
                 "(make a clone) and the grey hexagon (the off-left test):",
    stack=True,
    scripts=[
        script(
            when_flag(),
            hide(),
            forever(
                wait(pick_random(0.8, 2)),
                gap("make a new cactus", create_clone()),
            ),
            caption="Cactus (original): stay hidden, spawn a clone now and then",
        ),
        script(
            when_clone(),
            set_size(50),
            goto_xy(240, -55),
            show(),
            repeat_until(
                gap("has this cactus run off the left edge?",
                    lt(x_position(), -250)),
                changex(-6)),
            delete_clone(),
            caption="Each clone: run in from the right, then delete off the left",
        ),
    ],
    note="This is the falling rock from Scratch F, turned sideways and cloned. One "
         "rock became many cactuses: the hidden original is a \\emph{spawner}, and "
         "every clone runs the same short script on its own, then cleans itself up "
         "with \\blk{delete this clone}. Because the wait is random, the gaps vary; "
         "because a clone takes a couple of seconds to cross, two or three are "
         "usually on screen together. Keep the cactus speed the same as the ground "
         "or it looks like it is skating.",
    tasks=[
        ("Give the cactus 3 costumes and, right after \\blk{show}, add \\blk{switch "
         "costume to (pick random (1) to (3))}. Now each clone looks a little "
         "different.", "Cactuses vary in look instead of all being identical."),
        ("Random speed per cactus: at the top of the clone script pick a speed "
         "once into a \\blk{my speed} variable and use it in the loop, so each "
         "clone runs at its own pace.",
         "Some cactuses rush, some crawl - the timing is unpredictable."),
        ("Ramp it up: shorten the spawn wait as the game goes on (a smaller "
         "\\blk{pick random} range) so cactuses come thicker the longer you "
         "survive.", "The screen gets busier the further you get."),
    ],
)


# ---- Project 5: game over - the broadcast (fills the cliffhanger) ------------

p_msg = BUILD(
    "Game over: the broadcast",
    goal="Knock down the wall from the last piece. The cactus can spot a crash but "
         "cannot end the game alone. The fix is \\blk{broadcast}: it sends one "
         "message to the \\emph{whole} project, and every \\blk{when I receive} - on "
         "any sprite - runs at once. So the cactus shouts \\emph{game over}, and the "
         "Dino hears it and reacts. One signal, many sprites acting together - the "
         "one thing a lone sprite could never do.",
    setup="No new sprites. You finish the empty \\blk{if} on the \\textbf{cactus "
          "clone}, and add one \\blk{when I receive} script to the \\textbf{Dino}.",
    new_blocks=[
        ("broadcast [game over]", "Send the message \\emph{game over} to the whole project, then carry on - it does not wait. Make the message with the dropdown: \\emph{New message}."),
        ("when I receive [game over]", "A hat: the script under it runs the instant \\emph{game over} is broadcast - on this sprite or any other."),
        ("stop [all]", "Halt every script in the project - the score tick and all the clones included. Used last, after the game-over message is shown."),
    ],
    steps=[
        "Back to the \\textbf{cactus clone}. Fill the empty \\blk{if <touching "
        "[Dino]?>} with one block: \\blk{broadcast [game over]}. Make the message - "
        "click the dropdown, \\emph{New message}, name it \\texttt{game over}. Now a "
        "crash shouts to the whole project.",
        "The Dino listens. On the \\textbf{Dino} add a new script: \\blk{when I "
        "receive [game over]}, then \\blk{say (join (Game over! Score: ) (score))} "
        "to show the final score, and finally \\blk{stop [all]}.",
        "\\blk{stop [all]} is the \\emph{last} block on purpose: it freezes the "
        "score tick and removes every cactus and cloud clone - but only after the "
        "Dino has shown the game-over message, so the message is not cut off.",
        "Green flag. Survive and your score climbs; the first cactus that touches "
        "the Dino now broadcasts \\emph{game over}, the Dino shows your total, and "
        "everything halts. The game is complete.",
    ],
    script_intro="The two halves that close the loop: the cactus's crash now "
                 "broadcasts, and the Dino receives it:",
    stack=True,
    scripts=[
        script(
            when_clone(),
            set_size(50),
            goto_xy(240, -55),
            show(),
            repeat_until(
                lt(x_position(), -250),
                changex(-6),
                if_(touching("Dino"),
                    broadcast("game over"))),
            delete_clone(),
            caption="Cactus clone, completed: a crash now broadcasts game over",
        ),
        script(
            when_receive("game over"),
            say(join("Game over! Score: ", var("score"))),
            stop_all(),
            caption="Dino: on game over, show the score, then stop everything",
        ),
    ],
    note="This is the payoff. \\blk{broadcast} is a one-to-many shout: the cactus "
         "fires \\emph{game over} and moves on; every \\blk{when I receive [game "
         "over]} in the project runs at once - no sprite has to poll or watch a "
         "variable. Here only the Dino listens, but you could add \\blk{when I "
         "receive [game over]} to the clouds to freeze them, to a sound sprite to "
         "play a thud, to a \\emph{Game Over} banner to show itself - all from the "
         "single message. \\blk{stop [all]} comes last so the message is delivered "
         "and drawn before everything halts. (There is also \\blk{broadcast and "
         "wait}, which pauses the sender until listeners finish - not needed here.)",
    tasks=[
        ("Add a surprised look: give the Dino a \\blk{dino-hit} costume and, at the "
         "top of the \\blk{game over} script, \\blk{switch costume to [dino-hit]} "
         "before the \\blk{say}.", "The Dino pulls a shocked face the instant it "
         "crashes."),
        ("Freeze the sky too: add \\blk{when I receive [game over]} to the "
         "\\textbf{Cloud} with \\blk{stop [other scripts in sprite]}, so the clouds "
         "stop on the same message - one signal, many reactions.",
         "Everything stops together on the crash, not just the Dino."),
        ("Keep a high score: make a \\blk{best} variable, and on \\blk{game over} "
         "\\blk{if <(score) $>$ (best)>} then \\blk{set [best] to (score)}.",
         "The best run so far is remembered across games."),
    ],
)


# ---- Project 4: score, and spotting the crash (the cliffhanger) --------------

p3 = BUILD(
    "Score, and spotting the crash",
    goal="Two things here, and a cliffhanger. First a \\emph{score} that climbs "
         "while you survive - exactly like the real Chrome game, which counts how "
         "far you have run. Second, the cactus learns to \\emph{spot} the instant "
         "it hits the Dino. But spotting a crash and \\emph{acting} on it are "
         "different: a cactus clone can only control itself - it cannot make the "
         "Dino react or stop the game. So the crash is detected and then\\ldots "
         "nothing happens yet. That wall is exactly what the next piece knocks down.",
    setup="Make a variable \\textbf{score} \\emph{For all sprites}. You add one "
          "scoring script to the \\textbf{Dino}, and one \\blk{if} to the "
          "\\textbf{cactus clone}.",
    new_blocks=[
        ("change [score] by (1)", "Add one to the score. The Dino does this over and over while you are alive, so the score measures how long you have survived - Chrome scores the same way (distance run, not cactuses dodged)."),
        ("if <touching [Dino]?>", "Checked on a cactus clone: true the moment this cactus hits the Dino - the crash. For now its inside is empty: detecting the hit is easy, acting on it is the missing piece."),
    ],
    steps=[
        "The score lives on the \\textbf{Dino}: \\blk{when green flag clicked}, "
        "\\blk{set [score] to (0)}, then a \\blk{forever} with \\blk{wait (0.2) "
        "seconds} and \\blk{change [score] by (1)}. While you are alive the score "
        "climbs.",
        "Spotting the crash. Open the \\textbf{cactus clone} script. Inside the "
        "\\blk{repeat until} loop, under \\blk{change x by (-6)}, add \\blk{if "
        "<touching [Dino]?>}. The cactus can now \\emph{see} the moment it hits the "
        "Dino.",
        "But leave that \\blk{if} empty - and that is the point. What should happen "
        "on a crash? The game should end, the Dino should react, everything should "
        "stop. Yet a cactus clone can only move and delete \\emph{itself}; it has no "
        "way to reach the Dino or the score tick. Run it: touch a cactus and\\ldots "
        "nothing. We have hit the wall.",
        "That wall is what the next piece knocks down: a \\blk{broadcast} - one "
        "message every sprite hears at once - so a single crash can end the game "
        "for everybody.",
    ],
    script_intro="The Dino's score tick, and the cactus that now spots a crash - "
                 "its \\blk{if} is deliberately empty, waiting for the next piece:",
    stack=True,
    scripts=[
        script(
            when_flag(),
            set_var("score", 0),
            forever(
                wait(0.2),
                change_var("score", 1),
            ),
            caption="Dino: start at zero, then tick the score up while alive",
        ),
        script(
            when_clone(),
            set_size(50),
            goto_xy(240, -55),
            show(),
            repeat_until(
                lt(x_position(), -250),
                changex(-6),
                if_(touching("Dino"))),
            delete_clone(),
            caption="Cactus clone: run across and spot a hit - but it cannot act on it yet",
        ),
    ],
    note="The score is the easy half: the Dino counts time while alive, exactly how "
         "Chrome scores (distance, not cactuses dodged). The crash is the "
         "interesting half - and it stops mid-air on purpose. A clone is an island: "
         "it can change its own x and delete itself, and that is about all. It "
         "cannot tell the Dino to show \\emph{Game Over}, cannot stop the score "
         "tick, cannot reach the clouds. Detecting the crash is easy; getting that "
         "news to everyone is the missing tool - and that is the whole reason the "
         "next piece, \\blk{broadcast}, exists.",
    tasks=[
        ("Make the score climb faster as the game speeds up: use \\blk{change "
         "[score] by (speed)} instead of by 1 (once you have a \\blk{speed} "
         "variable).", "Score rises quicker the faster the world moves - long runs "
         "are rewarded."),
        ("Show the score on the stage: tick the checkbox next to the \\blk{score} "
         "variable so the number sits in the corner and climbs as you play.",
         "The live score is visible on the stage."),
    ],
)


ACTIVITIES = [p1, p_cloud, p2, p3, p_msg]
