# cs17

Curriculum-generation repo: Python generators (`gens/`) emit LaTeX worksheets (`worksheets/`). `scratchgen` is a Scratch-block DSL → scratch3 LaTeX (see `gens/scratchgen/`). Standalone build-along notes live in `misc/`.

## Scratch reference clones

Scratch's own source is cloned (shallow) **outside this repo** for verifying Scratch runtime behaviour when writing worksheets:

- `/Users/mdhussain/scratch-reference/scratch-vm` — block semantics, sprite state (`src/blocks/`, `src/sprites/rendered-target.js`)
- `/Users/mdhussain/scratch-reference/scratch-render` — rendering, bounds, fencing (`src/RenderWebGL.js`, `src/Skin.js`)

Re-clone if missing: `git clone --depth 1 https://github.com/scratchfoundation/{scratch-vm,scratch-render}.git`.

## Scratch gotcha: sprite fencing (a sprite can never go fully off-stage)

Every scripted motion block routes through `RenderedTarget.setXY` → `renderer.getFencedPositionOfDrawable` (`rendered-target.js:272`). It is **unconditional** — no block or flag disables it. Blocks affected: `change x/y by`, `set x/y to`, `go to x:y:`, `go to [mouse/random/sprite]`, `glide`.

Fence math (`RenderWebGL.js:1526`, `FENCE_WIDTH = 15`; `getFenceBounds` = untrimmed `getAABB`):

- `inset = floor(min(aabbWidth, aabbHeight) / 2)`
- `sx = 240 − min(15, inset)`  (x); `sy = 180 − min(15, inset)` (y)
- clamps so the untrimmed costume box always keeps `min(15, inset)` px on every edge.

**Consequence for scrolling backgrounds:** a full-stage-wide (480px, height ≥30) tile has `sx = 225`, so its centre bottoms out at **x ≈ −465**, never −480. A test like `if <(x position) < (-480)>` is unreachable. Two exactly-480 tiles can only span ~930px of travel but need 960 to leapfrog → structurally ~30px short → seam/flicker at any reachable threshold.

**Fix used (overlap, keeps the simple `change x by` leapfrog):** make each scenery tile **wider than the stage**. For a two-tile treadmill (spacing 480, jump 960, test `x position < -480`), the tile centre bottoms out at `-225 - W/2`; the `-480` test is both reachable AND the partner already covers the screen only when `W >= 495`. Use **W = 520** (centre reaches -485 so -480 fires; 40px overlap hides the seam). No script change vs the naive version — only the costume width. (Alternative, rejected as more machinery for a worse result: drive position from a scroll *variable*, which has no fence.) No vanilla un-fence block exists; TurboWarp mod removes fencing but that is not standard Scratch.

Fixed in worksheet `misc/dino_game_notes/dino_game_notes.py` Project 1 (moving ground): tiles are 520 wide.

## PRs

Follow global CLAUDE.md (PRs against `develop`, simple descriptions).
