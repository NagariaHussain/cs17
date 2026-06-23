#!/usr/bin/env python3
"""
slice_sprite.py — carve the combined Chrome-Dino sprite sheet into individual
transparent PNG costumes, ready to upload into Scratch.

    python3 slice_sprite.py                 # slice everything into assets/sliced/
    python3 slice_sprite.py --no-trim       # keep each box's exact bounds (don't shrink to ink)
    python3 slice_sprite.py --scale 2        # 2x bigger PNGs (nearest-neighbour, stays crisp)

Each REGION below is a verified box in assets/sprite.png given as INCLUSIVE pixel
bounds (x0, y0, x1, y1). `frames=N` splits the box into N equal-width sub-frames
(used for animation strips: dino run, pterodactyl flap, restart buttons).

By default every output is TIGHT-CROPPED to its non-transparent pixels. That
matters for Scratch: `touching?` collisions use non-transparent pixels, so
leftover padding makes hitboxes feel unfair (see REFERENCE_GAME.md gotcha #5).

Edit the REGIONS table to retune any box — the coordinates are the single source
of truth.
"""

import argparse
import os
from PIL import Image

SHEET = os.path.join(os.path.dirname(__file__), "assets", "sprite.png")
OUTDIR = os.path.join(os.path.dirname(__file__), "assets", "sliced")

# name, x0, y0, x1, y1 (inclusive), frames
# frames > 1 → split horizontally into `frames` equal slices, saved name_1.png …
REGIONS = [
    # --- dino poses (the player) ---
    ("dino_run",      1678,  2, 2117, 95, 5),  # 5 frames: idle (frame 1) + run cycle.
                                               # frame 1 doubles as the jump costume —
                                               # the standalone standing image at x76 is
                                               # skipped because it has a ground line
                                               # baked in that looks wrong mid-air.
    ("dino_dead",     2122,  6, 2201, 91, 1),  # crashed (X eyes) — Game Over costume
    ("dino_duck",     2206, 36, 2441, 95, 2),  # 2 ducking frames (optional)

    # --- obstacles ---
    # Cactus strips are pre-packed obstacle groups: a 1-, 2-, then 3-cactus
    # cluster laid side by side (this is exactly how Chrome's Obstacle.draw
    # indexes them by `size`). Small cells are 34px wide, large cells 50px.
    ("cactus_small_1", 446,  2,  479, 71, 1),  # single small cactus
    ("cactus_small_2", 480,  2,  547, 71, 1),  # pair
    ("cactus_small_3", 548,  2,  649, 71, 1),  # triple
    ("cactus_large_1", 652,  2,  701,101, 1),  # single large cactus
    ("cactus_large_2", 702,  2,  801,101, 1),  # pair
    ("cactus_large_3", 802,  2,  951,101, 1),  # triple
    ("pterodactyl",    260,  2,  443, 81, 2),  # 2 flap frames (optional flying obstacle)

    # --- UI / text ---
    ("game_over",     1294, 29, 1674, 49, 1),  # "GAME OVER" (letters are spaced out)
    ("digits",        1294,  2, 1531, 22, 1),  # 0123456789HI score font
    ("restart_circle", 151,135,  211,187, 1),  # circular-arrow restart icon
    ("restart_button", 218,130,  577,193, 5),  # 5 rounded restart buttons

    # --- ground / decor (optional) ---
    ("ground",           2,104, 2401,127, 1),  # full horizon line: flat line + pebbles + bumps
    ("cloud",          174,  2,  257, 28, 1),
    # moon: 7 phases (thin crescent -> full -> thin crescent), unequal widths,
    # cut at the thin "valleys" between crescents. The sparkle is a separate star.
    ("moon_1",         954,  2,  989, 81, 1),
    ("moon_2",         990,  2, 1029, 81, 1),
    ("moon_3",        1030,  2, 1070, 81, 1),
    ("moon_4",        1071,  2, 1154, 81, 1),  # full moon
    ("moon_5",        1155,  2, 1195, 81, 1),
    ("moon_6",        1196,  2, 1235, 81, 1),
    ("moon_7",        1236,  2, 1273, 81, 1),
    ("star",          1274,  2, 1291, 81, 1),
    ("chrome_icon",     10,134,   64,188, 1),
]

# Which sliced files map to the costumes REFERENCE_GAME.md asks for:
COSTUME_MAP = """
Scratch costume        ->  file(s) in assets/sliced/
  Dino  run1 / run2    ->  dino_run_3.png + dino_run_4.png  (alternating legs)
  Dino  jump / idle    ->  dino_run_1.png  (legs together, no ground line)
  Dino  dead           ->  dino_dead.png
  Cactus               ->  cactus_large_1.png  (single; _2/_3 are 2- and 3-cactus groups)
  GameOver text        ->  game_over.png
  Restart (optional)   ->  restart_circle.png
"""


def ink_bbox(img):
    """Bounding box of non-transparent pixels, or None if fully transparent."""
    alpha = img.split()[-1]
    return alpha.getbbox()


# Regions to clean of stray specks: the moon strip has tiny decorative star/dot
# pixels along its top & bottom edges that tight-cropping would otherwise keep.
DENOISE = {f"moon_{i}" for i in range(1, 8)}


def keep_largest_blob(img):
    """Keep only the largest 8-connected non-transparent component; clear the rest."""
    from collections import deque

    w, h = img.size
    px = img.load()
    seen = bytearray(w * h)
    best = []
    for sy in range(h):
        for sx in range(w):
            if px[sx, sy][3] < 16 or seen[sy * w + sx]:
                continue
            q = deque([(sx, sy)])
            seen[sy * w + sx] = 1
            cells = []
            while q:
                cx, cy = q.popleft()
                cells.append((cx, cy))
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        nx, ny = cx + dx, cy + dy
                        if (0 <= nx < w and 0 <= ny < h
                                and px[nx, ny][3] >= 16 and not seen[ny * w + nx]):
                            seen[ny * w + nx] = 1
                            q.append((nx, ny))
            if len(cells) > len(best):
                best = cells
    keep = set(best)
    for y in range(h):
        for x in range(w):
            if (x, y) not in keep:
                px[x, y] = (0, 0, 0, 0)
    return img


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-trim", action="store_true",
                    help="keep exact box bounds instead of shrinking to ink")
    ap.add_argument("--scale", type=int, default=1,
                    help="integer upscale factor (nearest-neighbour)")
    args = ap.parse_args()

    sheet = Image.open(SHEET).convert("RGBA")
    os.makedirs(OUTDIR, exist_ok=True)

    written = []
    for name, x0, y0, x1, y1, frames in REGIONS:
        # +1 because crop() is exclusive on the right/bottom edge
        for i in range(frames):
            fw = (x1 - x0 + 1) / frames
            fx0 = x0 + round(i * fw)
            fx1 = x0 + round((i + 1) * fw)
            crop = sheet.crop((fx0, y0, fx1, y1 + 1))

            if name in DENOISE:
                crop = keep_largest_blob(crop)

            if not args.no_trim:
                bb = ink_bbox(crop)
                if bb:
                    crop = crop.crop(bb)

            if args.scale > 1:
                crop = crop.resize(
                    (crop.width * args.scale, crop.height * args.scale),
                    Image.NEAREST,
                )

            fname = f"{name}.png" if frames == 1 else f"{name}_{i + 1}.png"
            crop.save(os.path.join(OUTDIR, fname))
            written.append((fname, crop.width, crop.height))

    print(f"Wrote {len(written)} files to {OUTDIR}:")
    for fname, w, h in written:
        print(f"  {fname:24s} {w}x{h}")
    print(COSTUME_MAP)


if __name__ == "__main__":
    main()
