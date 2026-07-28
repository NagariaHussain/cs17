#!/usr/bin/env python3
"""
slice_sprite.py — carve the combined Space-Invaders sprite sheet into individual
transparent PNG costumes, ready to upload into Scratch.

    python3 slice_sprite.py                 # slice everything into assets/sliced/
    python3 slice_sprite.py --no-trim       # keep each box's exact bounds (don't shrink to ink)
    python3 slice_sprite.py --scale 2        # 2x bigger PNGs (nearest-neighbour, stays crisp)

The source art (`assets/sheet.png`) is a true-alpha PNG, so each REGION below is
an INCLUSIVE pixel box (x0, y0, x1, y1) verified against the sheet. Unlike the
Dino sheet we don't split animation strips with `frames=N` — every invader here is
already drawn as two separate side-by-side frames, so each frame is its own box.

By default every output is TIGHT-CROPPED to its non-transparent pixels. That
matters for Scratch: `touching?` collisions use non-transparent pixels, so
leftover padding makes hitboxes feel unfair (see REFERENCE_GAME.md gotcha #5).

Edit the REGIONS table to retune any box — the coordinates are the single source
of truth. Regenerate the verification montage with:

    python3 slice_sprite.py && python3 -c "import slice_sprite as s; s.montage()"
"""

import argparse
import os
from PIL import Image

SHEET = os.path.join(os.path.dirname(__file__), "assets", "sheet.png")
OUTDIR = os.path.join(os.path.dirname(__file__), "assets", "sliced")

# name, x0, y0, x1, y1  (inclusive pixel bounds in assets/sheet.png)
REGIONS = [
    # --- Row 1: the marching fleet, front ranks (each invader = 2 animation frames) ---
    ("invader_green_1",    50,  51,  155, 134), ("invader_green_2",   183,  51,  291, 132),
    ("invader_cyan_1",    329,  51,  423, 133), ("invader_cyan_2",    449,  51,  545, 133),
    ("invader_blue_1",    597,  51,  700, 133), ("invader_blue_2",    725,  51,  827, 133),
    ("invader_magenta_1", 862,  51,  952, 134), ("invader_magenta_2", 978,  51, 1069, 134),
    ("invader_pink_1",   1118,  51, 1210, 134), ("invader_pink_2",   1241,  51, 1334, 134),
    ("invader_pink_3",   1372,  51, 1467, 134),

    # --- Row 2: rear ranks + the first saucer ---
    ("invader_red_1",      50, 177,  155, 249), ("invader_red_2",     190, 177,  294, 247),
    ("invader_crab_1",    330, 177,  424, 250), ("invader_crab_2",    452, 177,  547, 250),
    ("invader_yellow_1",  600, 177,  696, 250), ("invader_yellow_2",  725, 177,  817, 250),
    ("invader_lime_1",    861, 177,  954, 250), ("invader_lime_2",    979, 177, 1074, 247),
    ("saucer_silver_1",  1151, 178, 1259, 250), ("saucer_silver_2",  1326, 177, 1436, 250),

    # --- Row 3: big enemies / minibosses (the wide battlecruiser is one sprite) ---
    ("lander_purple_1",    42, 310,  202, 407), ("lander_purple_2",   218, 312,  402, 407),
    ("battlecruiser",     450, 301,  707, 407),
    ("crab_red_1",        757, 304,  891, 410), ("crab_red_2",        920, 305, 1072, 409),
    ("saucer_boss_1",    1115, 299, 1270, 410), ("saucer_boss_2",    1317, 299, 1470, 409),

    # --- Row 4: player ships + projectiles ---
    ("ship_fighter_1",     43, 459,  146, 561), ("ship_fighter_2",    165, 459,  270, 561),
    ("ship_fighter_3",    295, 459,  402, 561), ("ship_fighter_4",    419, 459,  531, 561),
    ("ship_delta_1",      576, 463,  719, 561), ("ship_delta_2",      733, 461,  867, 560),
    ("bullet_cyan_1",     913, 464,  928, 559), ("bullet_cyan_2",     952, 464,  966, 559),
    ("bullet_orange_1",  1040, 464, 1055, 559), ("bullet_orange_2",  1081, 463, 1095, 561),
    ("bullet_green_1",   1170, 464, 1185, 559), ("bullet_green_2",   1210, 464, 1224, 557),
    ("bullet_magenta_1", 1305, 464, 1319, 559), ("bullet_magenta_2", 1346, 461, 1361, 555),
    ("orb_plasma",       1416, 480, 1478, 541),

    # --- Row 5: pickups / power-ups / HUD flags ---
    ("pickup_heart",       49, 607,  114, 668), ("pickup_star",       171, 608,  233, 668),
    ("pickup_shield",     284, 607,  341, 668), ("pickup_wrench",     407, 607,  477, 668),
    ("pickup_boost",      536, 607,  591, 668), ("badge_s",           668, 607,  731, 668),
    ("badge_p",           790, 607,  851, 668),
    ("flag_red",          929, 607,  985, 668), ("flag_orange",      1038, 607, 1092, 668),
    ("flag_green",       1145, 607, 1197, 668), ("flag_blue",        1234, 607, 1286, 667),
    ("flag_purple",      1341, 608, 1392, 668), ("pickup_battery",   1439, 607, 1479, 668),

    # --- Row 6: explosion (4 frames) + planets + gems + bonus UFO ---
    ("explosion_1",        52, 710,  128, 791), ("explosion_2",      187, 712,  283, 799),
    ("explosion_3",       323, 703,  446, 801), ("explosion_4",      490, 704,  605, 799),
    ("planet_brown",      653, 712,  747, 799), ("planet_gray",      805, 712,  900, 799),
    ("planet_purple",     955, 708, 1046, 799),
    ("gem_blue",         1121, 719, 1177, 799), ("gem_yellow",       1235, 714, 1291, 799),
    ("ufo_purple",       1345, 728, 1466, 791),

    # --- Row 7: UI text (the two split words are merged back into one costume each) ---
    ("text_game_over",     51, 856,  469, 918),   # "GAME" + "OVER"
    ("text_you_win",      538, 856,  895, 918),   # "YOU" + "WIN!"
    ("text_ready",        963, 856, 1210, 918),
    ("life_1",           1263, 856, 1327, 918), ("life_2", 1345, 856, 1409, 918),
    ("life_3",           1424, 856, 1489, 918),
]

# Which sliced files map to the costumes REFERENCE_GAME.md asks for:
COSTUME_MAP = """
Scratch sprite / costume        ->  file(s) in assets/sliced/
  Invader  inv_a / inv_b        ->  invader_green_1.png + invader_green_2.png  (the wiggle;
                                     any *_1/_2 colour pair works — one colour per row rank)
  Player   ship                 ->  ship_fighter_1.png  (or ship_delta_1 for the arrow look)
  Bullet   laser                ->  bullet_cyan_1.png   (cyan/orange/green/magenta variants)
  UFO / mothership (bonus)      ->  ufo_purple.png  or  saucer_boss_1.png
  Explosion (invader die)       ->  explosion_1..4.png  (play as a 4-frame animation)
  GameOver text                 ->  text_game_over.png
  YouWin text                   ->  text_you_win.png
  READY? / lives HUD (optional) ->  text_ready.png, life_1.png, pickup_heart.png
"""


def ink_bbox(img):
    """Bounding box of non-transparent pixels, or None if fully transparent."""
    return img.split()[-1].getbbox()


def slice_all(no_trim=False, scale=1):
    sheet = Image.open(SHEET).convert("RGBA")
    os.makedirs(OUTDIR, exist_ok=True)
    written = []
    for name, x0, y0, x1, y1 in REGIONS:
        crop = sheet.crop((x0, y0, x1 + 1, y1 + 1))   # +1: crop is exclusive on right/bottom
        if not no_trim:
            bb = ink_bbox(crop)
            if bb:
                crop = crop.crop(bb)
        if scale > 1:
            crop = crop.resize((crop.width * scale, crop.height * scale), Image.NEAREST)
        crop.save(os.path.join(OUTDIR, f"{name}.png"))
        written.append((name, crop.width, crop.height))
    return written


def montage(cols=8, cell=140, pad=8):
    """Lay every sliced PNG on a dark grid with labels — visual QA of the cut."""
    from PIL import ImageDraw
    files = [f"{n}.png" for n, *_ in REGIONS]
    rows = (len(files) + cols - 1) // cols
    W, H = cols * cell, rows * (cell + 16)
    board = Image.new("RGBA", (W, H), (22, 22, 28, 255))
    d = ImageDraw.Draw(board)
    for i, f in enumerate(files):
        im = Image.open(os.path.join(OUTDIR, f)).convert("RGBA")
        s = min((cell - pad) / im.width, (cell - pad) / im.height, 1.0)
        im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.NEAREST)
        cx = (i % cols) * cell + cell // 2
        cy = (i // cols) * (cell + 16) + cell // 2
        board.alpha_composite(im, (cx - im.width // 2, cy - im.height // 2))
        d.text((cx - cell // 2 + 3, (i // cols) * (cell + 16) + cell - 2),
               f[:-4], fill=(230, 230, 235, 255))
    out = os.path.join(OUTDIR, "_montage.png")
    board.convert("RGB").save(out)
    print("wrote", out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-trim", action="store_true",
                    help="keep exact box bounds instead of shrinking to ink")
    ap.add_argument("--scale", type=int, default=1,
                    help="integer upscale factor (nearest-neighbour)")
    args = ap.parse_args()
    written = slice_all(no_trim=args.no_trim, scale=args.scale)
    print(f"Wrote {len(written)} files to {OUTDIR}:")
    for name, w, h in written:
        print(f"  {name + '.png':24s} {w}x{h}")
    print(COSTUME_MAP)


if __name__ == "__main__":
    main()
