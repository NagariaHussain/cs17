# Space Invaders in Scratch — Full Reference Build

This is the **finished game** (the "Day 5" version). Build this first and confirm it
works end-to-end. Once it works, we carve it back into Day 0 → Day 5 for teaching.

Everything here uses **stock Scratch 3 blocks only** — no extensions.

> This is the natural step *up* from the Dino build. Dino taught *one* sprite becoming
> *many* clones. Invaders teaches the next thing: **many clones that must act as one
> organism** — a fleet that marches, drops, and reverses in lockstep — plus the idea
> the Dino never touched: **the player shoots back**.

---

## The one design idea that makes this easy

**Many clones, one brain.**

There are 55 invaders on screen, but there is not 55 of anything in your code. There is
**one Invader sprite** that stamps out 55 clones, and a set of **global variables**
(`invaderDir`, `hitEdge`) that every clone reads so the whole fleet turns together. A
single hidden "conductor" beats time with `broadcast … and wait`; the clones just obey.

The same trick powers the shooting: your laser isn't a drawn line, it's **one Bullet
clone** flying up, and an invader dies when it's `touching [Bullet]?`. Teach this out
loud — "if there are lots of them on screen, it's clones" is the transferable insight,
exactly like "the world moves toward the dino" was last time.

---

## Stage setup

- **Backdrop:** plain black (space). Optional: a few scattered white dots for stars,
  or the classic green floor line near the bottom.
- **Stage size:** default (480 × 360). x runs -240…240, y runs -180…180.

### The two reference lines

- **Player row** at **y = -150**: the ship slides left/right along here and never
  leaves it.
- **Invasion line** at **y = -120**: if the marching fleet ever drops this low, the
  invasion succeeds and it's game over. Keep both numbers consistent everywhere.

---

## Sprites

| Sprite | Role | Costume notes |
|---|---|---|
| **Player** | Your ship. Slides left/right on one row, fires up. | `ship_fighter_1` (or `ship_delta_1` for the arrow look). |
| **Invader** | The fleet. One sprite → 55 marching clones. | 2 costumes for the classic wiggle — any colour pair, e.g. `invader_green_1`/`invader_green_2`. Start hidden. |
| **Bullet** | Your laser. One clone flies up per shot. | `bullet_cyan_1` (cyan/orange/green/magenta all provided). Start hidden. |
| **GameOver** | "Game Over" text. | `text_game_over`. Start hidden. |
| **YouWin** | "You Win" text. | `text_you_win`. Start hidden. |

Optional advanced sprites (see *Polish*): **Bomb** (invader return fire), **UFO** (the
bonus mothership — `ufo_purple` or `saucer_boss_1`), **Shield** (erodable bunkers). A
4-frame `explosion_1..4` is included if you want a death puff when an invader is hit.

## Assets (slicing the sheet)

All costumes are pre-cut from one art sheet. `assets/sheet.png` is the combined
true-alpha sprite sheet; **`slice_sprite.py`** carves it into individual transparent
PNGs in `assets/sliced/`, each tight-cropped to its pixels so Scratch hitboxes are fair:

```bash
python3 slice_sprite.py            # -> assets/sliced/*.png
python3 slice_sprite.py --scale 2  # 2x bigger, still crisp (nearest-neighbour)
```

The sheet gives you a whole game's worth of parts: **10 invader colours** (each a 2-frame
pair), silver/boss saucers, a wide `battlecruiser` miniboss, **6 player ships**, four
bullet colours plus an `orb_plasma`, pickups (`pickup_heart`, `pickup_shield`,
`pickup_star`, …), HUD `flag_*` and `life_*` icons, planets/gems for backdrops, the
`explosion_1..4` animation, and the `text_game_over` / `text_you_win` / `text_ready`
banners. Upload each PNG onto the matching sprite via the **Costumes** tab → *Upload
Costume*. The name→file map lives at the bottom of `slice_sprite.py` (`COSTUME_MAP`).

---

## Sounds

Space Invaders has one of the most famous soundtracks in games — a **four-note
descending bass loop that speeds up as the fleet does**. Drop the effects in
`assets/sounds/` and import each `.mp3` onto the right sprite via the **Sounds** tab →
*Upload Sound* (Scratch accepts MP3/WAV, not Ogg). A sound can only be used by the
sprite it's loaded into.

| File | Import onto | Plays when |
|---|---|---|
| `shoot.mp3`         | **Bullet** | you fire |
| `invader_die.mp3`   | **Invader**| a clone is hit |
| `player_die.mp3`    | **Player** | the fleet reaches you / touches you |
| `march.mp3`         | **Invader**| once per fleet step (the bass note) |

> `start sound [ … ]` fires the sound and lets the script keep running (no wait).
> Use `play sound [ … ] until done` only when you want everything to pause for it.

Free, permissively-licensed sprites and sounds are easy to find — e.g. the
"Assets for a space invader-like game" and "Pixel Space Invaders" packs on
OpenGameArt.org (player ship, aliens, bullets, explosions in one sheet).

---

## Variables

### Global — "For all sprites"

Make these under the **Variables** category → *Make a Variable* → **For all sprites**.

| Variable | Meaning | Why it exists |
|---|---|---|
| `score`        | Points, one per kill | Reward |
| `invadersLeft` | How many invaders are still alive | Wins the game at 0 **and** drives the speed-up |
| `invaderDir`   | Fleet direction: `1` = right, `-1` = left | One number turns the whole army |
| `invaderStep`  | Pixels the fleet moves each march | Difficulty knob |
| `hitEdge`      | Did any invader touch the edge this march? (0/1) | Lets one clone tell the conductor to reverse |
| `bulletActive` | Is one of our lasers already in the air? (0/1) | Enforces "one shot on screen" |

> These must be global because the **conductor** sets `invaderDir`/`hitEdge` while the
> **clones** read them, and the **Bullet** reads/writes `bulletActive` that the whole
> game shares. This is the same "keep it global for beginners" call we made in Dino.

### Local — "For this sprite only"

Make **one** variable on the **Invader** sprite as **For this sprite only**:

| Variable | Meaning | Why it exists |
|---|---|---|
| `me` | Am I a real clone (1) or the hidden conductor (0)? | Stops the conductor from marching itself |

> **This is the new concept.** A *for-this-sprite-only* variable is **copied into each
> clone and then owned by that clone** — 55 independent `me`s. The conductor keeps its
> `me = 0`; every clone sets its own to `1`. That one line is how the fleet's brain
> tells itself apart from its body. Dino never needed this; Invaders lives on it.

---

## Custom block (My Blocks)

Create one custom block on the **Invader** sprite: **`spawn invader (x) (y)`** — with
two number inputs. This is the abstraction we introduce on Day 3; the finished game
already uses it to stamp the grid.

```
define spawn invader (x) (y)
go to x: (x) y: (y)              // the clone inherits THIS position at birth
create clone of [myself v]
change [invadersLeft v] by (1)
```

> The reliable way to place a clone: **move the original to where you want it, *then*
> clone.** A new clone is born at its parent's current position, so there's no race —
> the same reason we don't read shared "spawnX" variables from inside the clone.

---

## Player — scripts

### 1) Setup + movement

```
when green flag clicked
show
go to x: (0) y: (-150)
set [score v] to (0)
forever
  if < key [left arrow v] pressed? > then
    change x by (-6)
  end
  if < key [right arrow v] pressed? > then
    change x by (6)
  end
  if < (x position) > (220) > then set x to (220)      // stay on screen
  if < (x position) < (-220) > then set x to (-220)
end
```

> Note the contrast with Dino out loud: **the Dino never moved sideways; the world
> moved. The ship *does* move sideways, but the world (the fleet) also comes to it.**

### 2) Losing when touched

```
when green flag clicked
forever
  if < touching [Invader v] ? > then
    broadcast [game over v]
  end
end
```

---

## Bullet — scripts

### 1) Setup

```
when green flag clicked
hide
set [bulletActive v] to (0)
```

### 2) Fire (with the "one shot on screen" rule)

```
when [space v] key pressed
if < (bulletActive) = (0) > then       // only if no laser is currently flying
  set [bulletActive v] to (1)
  go to [Player v]                     // jump to the ship's muzzle
  create clone of [myself v]
  start sound [shoot v]
end
```

> `bulletActive` is exactly the same *state-flag* idea as Dino's `grounded?`: a 0/1
> variable that gates an action. The real 1978 arcade game allowed **one player shot at
> a time** too — this isn't a simplification, it's authentic.

### 3) Each laser's life

```
when I start as a clone
show
forever
  change y by (10)
  if < touching [Invader v] ? > then    // hit something → clean up
    set [bulletActive v] to (0)
    delete this clone
  end
  if < (y position) > (180) > then       // flew off the top → clean up
    set [bulletActive v] to (0)
    delete this clone
  end
end
```

> Both the bullet **and** the invader check `touching?` (see below). Whichever notices
> first, the other's check tidies up its own sprite. Resetting `bulletActive` here is
> what lets you fire the *next* shot.

---

## Invader — scripts

The Invader sprite plays two roles: the hidden **conductor** (the original) builds the
fleet and beats time, and each **clone** is one marching alien.

### 1) Conductor: build the fleet, then beat time

```
when green flag clicked
set [me v] to (0)                        // I am the conductor, not a clone
hide
set [invaderDir v]   to (1)
set [invaderStep v]  to (12)
set [invadersLeft v] to (0)
set [score v]        to (0)

set [row v] to (0)                       // 5 rows...
repeat (5)
  set [col v] to (0)                     // ...of 11 = 55 invaders (the real number)
  repeat (11)
    spawn invader ( (-200) + ( (col) * (40) ) ) ( (150) - ( (row) * (28) ) )
    change [col v] by (1)
  end
  change [row v] by (1)
end

forever                                  // the conductor's heartbeat
  wait ( (0.05) + ( (invadersLeft) / (120) ) ) seconds   // <-- the famous speed-up
  set [hitEdge v] to (0)
  broadcast [march v] and wait           // every clone steps once; wait for all of them
  if < (hitEdge) = (1) > then
    broadcast [dropdown v] and wait       // ...then, if anyone hit the wall, drop + turn
    set [invaderDir v] to ( (0) - (invaderDir) )
  end
  if < (invadersLeft) = (0) > then
    broadcast [you win v]
    stop [all v]
  end
end
```

> `row` and `col` are throwaway counters — make them global or local, it doesn't matter.
> The grid math (`-200 + col*40`, `150 - row*28`) is pure **Operators**; walk through
> one cell out loud so students see where each alien lands.

### 2) Clone: come alive

```
when I start as a clone
set [me v] to (1)                        // I am a real invader
show
forever
  if < touching [Bullet v] ? > then
    change [score v] by (10)
    change [invadersLeft v] by (-1)
    start sound [invader die v]
    delete this clone
  end
end
```

### 3) Clone: march when the conductor says so

```
when I receive [march v]
if < (me) = (1) > then                    // conductor ignores its own baton
  change x by ( (invaderDir) * (invaderStep) )
  next costume                            // the classic two-frame wiggle
  if < ( (x position) * (invaderDir) ) > (215) > then
    set [hitEdge v] to (1)                // I'm at the wall — tell everyone
  end
end
```

> `(x position) * (invaderDir) > 215` is one condition that covers **both** walls:
> going right (`dir = 1`) it means `x > 215`; going left (`dir = -1`) it means
> `x < -215`. Same flavour of maths trick as Dino's `(0) - (speed)`. Any *one* invader
> setting `hitEdge` is enough — the conductor reverses the *whole* fleet next tick.

### 4) Clone: drop and threaten the invasion line

```
when I receive [dropdown v]
if < (me) = (1) > then
  change y by (-16)
  if < (y position) < (-120) > then       // reached your row → they've landed
    broadcast [game over v]
  end
end
```

---

## The famous speed-up — and why it's a bug we're copying on purpose

The single most iconic thing about Space Invaders is that **the aliens accelerate as
you kill them**. In the 1978 arcade original, Tomohiro Nishikado's hardware could only
redraw so many sprites per frame. With 55 invaders on screen, updating them all was
slow, so the fleet crept. As you destroyed them, there were fewer left to draw, the
CPU finished the frame sooner, and the survivors **sped up all on their own.** It was
an accident of the hardware that turned out to be the best difficulty curve in arcade
history — so every later version kept it deliberately.

We reproduce it in one line, in the conductor's heartbeat:

```
wait ( (0.05) + ( (invadersLeft) / (120) ) ) seconds
```

55 invaders → wait ≈ 0.51 s between marches (slow, menacing). 1 invader → wait ≈
0.06 s (frantic). The last alien is always the scariest — for free, from the same
count we use to detect the win. Tune the `/ 120` until the panic feels right.

This is the perfect callback to Dino's difficulty ramp: **there, difficulty rose with
`score`; here it rises as `invadersLeft` falls.** Same idea, opposite direction.

---

## Polish (optional Day-5 extras)

Each of these is one more sprite that reuses patterns the class already owns.

- **Return fire (Bomb).** A **Bomb** sprite, mirror image of the Bullet: on a rare
  `if <(pick random (1) to (400)) = (1)>` inside an invader's loop, `go to` that
  invader and `create clone of [Bomb v]`, and the bomb clone falls (`change y by (-6)`)
  until it hits the player or the floor. Now the player can lose to a shot, not just to
  the landing.
- **The mothership (UFO).** A **UFO** sprite that, every ~20 seconds, slides across the
  very top for bonus points if you tag it. Pure Dino-style "world slides past" movement.
- **Shields / bunkers.** Four **Shield** sprites low on the screen that erode: when a
  bomb or bullet touches one, stamp a transparent "bite" out of its costume. This is the
  advanced one — it needs the pen/costume-editing idea — so save it for a keen group.

---

## GameOver / YouWin sprites — scripts

```
GameOver:
when green flag clicked
hide

when I receive [game over v]
go to x: (0) y: (0)
show
play sound [player die v] until done      // put player_die on the Player, or here
stop [all v]
```

```
YouWin:
when green flag clicked
hide

when I receive [you win v]
go to x: (0) y: (0)
show
```

> As in Dino, use **broadcast … *and wait*** for `game over` if you want the text to
> land before `stop all` freezes the screen. The `stop all` is what ends the game.

---

## Restart

Pressing the **green flag** restarts everything — every script hooks `when green flag
clicked`, and the conductor rebuilds all 55 clones from scratch. That's the whole
restart mechanism, no extra code. Same "it's free" moment as Dino; kids love it.

---

## Tuning cheatsheet (the numbers you'll fiddle with)

| Feel | Knob |
|---|---|
| Fleet marches too slow / fast overall | the `0.05` base and `/ 120` in the conductor wait |
| Whole game too easy / hard | `invaderStep` (12) and the drop distance (`-16`) |
| Ship too sluggish / twitchy | the `change x by (±6)` in the Player loop |
| Can't rapid-fire (or fires too much) | the `bulletActive` rule — remove it for machine-gun mode |
| Lasers too slow to reach the top | `change y by (10)` on the bullet |
| Grid too wide / tall for the stage | the `40` (column gap) and `28` (row gap) in the build loop |
| Reverses feel jittery at the wall | the `215` edge threshold |

---

## Known gotchas (these are also your lesson hooks)

1. **The whole fleet flips direction 55 times at once.** If every clone reverses
   `invaderDir` itself, they fight each other and jitter in place. Fix: any clone only
   *reports* `hitEdge`; the **one** conductor reverses direction **once**. This is the
   headline lesson of the project — coordination through a shared variable.
2. **The conductor marches itself off the screen.** Without the `me` flag, the hidden
   original also obeys `march`, drifts to the wall, and sets `hitEdge` forever so the
   fleet keeps dropping. The *for-this-sprite-only* `me` is the fix.
3. **Machine-gun bug.** Without `bulletActive`, holding space sprays a wall of lasers
   and every invader dies instantly. The state flag gates you to one shot — just like
   `grounded?` gated the Dino to one jump.
4. **Clones spawn in a pile.** If the clone reads a shared `spawnX` variable *after*
   birth, the build loop has already moved on. Fix: position the original, *then* clone
   — the clone inherits that spot. (This is why `spawn invader` does `go to` first.)
5. **Hitboxes ≠ pictures.** `touching?` uses non-transparent pixels, so costume padding
   makes shots feel like they miss. Trim the invader and bullet costumes.
6. **You "win" the instant you start.** If you forget to `change invadersLeft by (1)`
   in `spawn invader`, the count is 0 and the conductor broadcasts *you win* on frame
   one. Count them up as you build them.

---

## How this maps to the teaching days

| Day | What's on screen | New concept | What we *remove* from this reference to get there |
|---|---|---|---|
| 0 | One invader slides left, drops, comes back | sequence, `forever`, `change x`, reverse at edge | clones, player, bullets, fleet, score |
| 1 | A ship you can drive; a bullet you can fire | `if` + key sensing, `go to sprite`, first clone | fleet, marching, collision, score |
| 2 | Shooting a single invader scores + kills it | **conditionals**, `touching?`, `bulletActive` state flag | the fleet (still just one invader), difficulty |
| 3 | A whole 5×11 grid, built cleanly | **My Blocks with inputs** + nested loops (`spawn invader x y`) | marching coordination, speed-up |
| 4 | The grid marches, drops, and turns as one | **clone coordination** via globals + `me`, `broadcast … and wait` | the speed-up, win/lose polish |
| 5 | It accelerates; you can win or lose; polish | operators, game state, game feel (+ optional bombs/UFO/shields) | — (this full build) |

Each day = "here's the limited version → feel the pain → learn the tool that fixes it."
The spine of the course is unchanged from Dino; only the tools at Days 3–4 level up from
*making* clones to *coordinating* them.
