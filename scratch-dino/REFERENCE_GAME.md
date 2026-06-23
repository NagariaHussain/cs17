# Chrome Dino in Scratch — Full Reference Build

This is the **finished game** (the "Day 5" version). Build this first and confirm it
works end-to-end. Once it works, we carve it back into Day 0 → Day 5 for teaching.

Everything here uses **stock Scratch 3 blocks only** — no extensions.

---

## The one design idea that makes this easy

**The dino never moves left or right. The world moves toward the dino.**

The dino stays at a fixed x on the left and only moves *up and down* (jumping).
The cactuses spawn on the right and slide left. This is exactly how the real Chrome
game works, and it makes every script dramatically simpler. Teach this out loud — it's
a transferable game-dev insight.

---

## Stage setup

- **Backdrop:** plain white. Draw one horizontal **ground line** across the bottom
  (around y = -80). Optional: a second light-grey line for texture.
- **Stage size:** default (480 × 360). x runs -240…240, y runs -180…180.

### Ground reference

We put the "floor" at **y = -80**. The dino rests there; cactuses sit there too, so
their bodies overlap horizontally and collisions register. Keep this number consistent
everywhere.

---

## Sprites

| Sprite | Role | Costume notes |
|---|---|---|
| **Dino** | Player. Stationary at left, jumps. | Use the Scratch cat or any sprite; ideally 2 costumes (`run1`/`run2`) for a running animation. |
| **Cactus** | Obstacle. Spawns clones on the right. | One simple costume. Start hidden. |
| **GameOver** | "Game Over" text. | A text costume (use the Text tool). Start hidden. |

---

## Sounds

Three sound effects ripped straight from the real Chrome game live in
`assets/sounds/`. In Scratch, a sound can only be used by the sprite it's loaded
into, so import each `.ogg` onto the right sprite via the **Sounds** tab →
*Upload Sound*:

| File | Import onto | Plays when |
|---|---|---|
| `jump.ogg`      | **Dino**   | the dino jumps |
| `game_over.ogg` | **Dino**   | the dino hits a cactus |
| `score.ogg`     | **Cactus** | you clear a cactus (the `+1` moment) |

> `start sound [ … ]` fires the sound and lets the script keep running (no wait).
> Use `play sound [ … ] until done` only when you want everything to pause for it.

---

## Variables (all "For all sprites")

Make these four under the **Variables** category → *Make a Variable*.

| Variable | Meaning | Why it exists |
|---|---|---|
| `velocity` | Dino's vertical speed this frame | The heart of the jump — makes gravity feel real |
| `score`    | Points, climbs over time | Reward + drives difficulty |
| `speed`    | How fast cactuses move left | Lets the game get harder |
| `grounded?`| Is the dino on the floor? (0/1) | Prevents mid-air double-jumps |

> All four are global ("For all sprites") because the **Cactus** sprite needs to read
> `speed`. Keeping them all global avoids a second concept for beginners.

---

## Custom block (My Blocks)

Create one custom block on the **Dino** sprite: **`jump`** (no inputs).
This is the abstraction we introduce on Day 3 — the finished game already uses it.

```
define jump
if < (grounded?) = (1) > then
  set [velocity v] to (13)
  set [grounded? v] to (0)
  start sound [jump v]                  // only when we actually leave the ground
end
```

---

## Dino — scripts

The Dino runs **four scripts at once** (Scratch runs them in parallel — itself a nice
teaching point).

### 1) Setup

```
when green flag clicked
go to x: (-150) y: (-80)
set [velocity v] to (0)
set [grounded? v] to (1)
set [score v]    to (0)
set [speed v]    to (5)
```

### 2) Gravity loop (the core physics)

```
when green flag clicked
forever
  change y by (velocity)
  change [velocity v] by (-1)          // gravity pulls velocity down every frame
  if < (y position) < (-80) > then     // hit the floor?
    set y to (-80)
    set [velocity v] to (0)
    set [grounded? v] to (1)
  end
end
```

### 3) Jump on key press

```
when [space v] key pressed
jump
```

(Optional second trigger: duplicate with `up arrow`.)

### 4) Collision → game over

```
when green flag clicked
forever
  if < touching [Cactus v] ? > then
    broadcast [game over v] and wait        // show the "Game Over" text first
    play sound [game over v] until done      // let the hit sound finish before...
    stop [all v]                             // ...stop all silences everything
  end
end
```

> Use **broadcast … *and wait*** so the "Game Over" text actually appears before
> `stop all` freezes everything.

### 5) (Optional) running animation

```
when green flag clicked
forever
  next costume
  wait (0.15) seconds
end
```

---

## Cactus — scripts

### 1) Spawner

```
when green flag clicked
hide
forever
  wait (pick random (1.0) to (2.0)) seconds
  create clone of [myself v]
end
```

### 2) Each clone's life

```
when I start as a clone
go to x: (240) y: (-80)
show
forever
  change x by ( (0) - (speed) )        // move left by 'speed' pixels per frame
  if < (x position) < (-240) > then
    change [score v] by (1)            // survived one cactus → +1
    start sound [score v]              // little "ping" for clearing it
    delete this clone
  end
end
```

> `(0) - (speed)` is the **Operators** subtraction block with `speed` dropped into the
> right slot. That's how you move left by a positive variable.

---

## Difficulty ramp (put this on the Stage, or on the Dino as a 5th script)

```
when green flag clicked
forever
  wait (2) seconds
  set [speed v] to ( (5) + ( (score) / (5) ) )   // faster as score climbs
end
```

Tune the `/ 5` until it feels right.

---

## GameOver sprite — scripts

```
when green flag clicked
hide

when I receive [game over v]
go to x: (0) y: (0)
show
```

---

## Restart

Pressing the **green flag** restarts everything (every script hooks `when green flag
clicked`). That's the whole restart mechanism — no extra code needed. Mention this; kids
love that it's "free."

---

## Tuning cheatsheet (the numbers you'll fiddle with)

| Feel | Knob |
|---|---|
| Jump too low / can't clear cactus | raise `velocity` impulse in `jump` (try 13 → 15) |
| Falls too floaty / too fast | change gravity `change velocity by (-1)` (try -1 → -2) |
| Cactuses too easy / hard | starting `speed` (5) and the spawn `wait` range (1.0–2.0) |
| Game too easy late | the `/ 5` in the difficulty ramp |
| Collision feels unfair | shrink the cactus costume's transparent margins, or the dino's |

---

## Known gotchas (these are also your lesson hooks)

1. **No gravity = teleporting dino.** If you skip `velocity` and just `change y by 80`
   then `-80`, the dino snaps up and down with no arc. The `velocity` variable is the fix
   — and the single most important concept in the course.
2. **Double-jump bug.** Without `grounded?`, holding/spamming space lets the dino fly. The
   flag gates it to one jump per landing.
3. **Game Over never shows.** Caused by `stop all` running before the broadcast is handled.
   Fixed by `broadcast … and wait`.
4. **Only one cactus.** Looping a single sprite is predictable and fake. **Clones** give
   an endless, randomly-timed stream from one sprite — the big "whoa" of the project.
5. **Hitboxes ≠ pictures.** `touching?` uses non-transparent pixels, so costume padding
   makes collisions feel off. Trim costumes.

---

## How this maps to the teaching days

| Day | What's on screen | New concept | What we *remove* from this reference to get there |
|---|---|---|---|
| 0 | A cactus slides past | sequence, `forever`, `change x` | everything except one moving cactus |
| 1 | Dino jumps (with gravity) | **variables**, velocity/gravity | collision, clones, score, custom block |
| 2 | You can lose; score counts | **conditionals**, `touching?`, sensing | clones, custom block, difficulty ramp |
| 3 | Same game, cleaner code | **My Blocks** (abstraction) + inputs | clones, difficulty ramp |
| 4 | Many random cactuses | **clones** + `pick random` | difficulty ramp |
| 5 | It gets harder; polish | operators, state, game feel | — (this full build) |

Each day = "here's the limited version → feel the pain → learn the tool that fixes it."
```
