"""
Update all map assets from the source map.png.

This script is the one-stop pipeline for propagating map changes.
Starting from assets/maps/map.png it will:

  1. Resize to 1000x550 → minimap.png (lossless PNG)
  2. Slice map.png into 1024x1024 center-origin tiles
  3. Save tiles into tiles_q100 (lossless), tiles_q95, tiles_q70,
     tiles_q10
  4. Write tile-manifest.json

Usage:
  python scripts/update-map-from-full-map-png.py

Requires: pip install Pillow
"""

import os
import sys
import json
import math
import shutil
import time
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

# ── Paths (relative to this script in /scripts) ────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_DIR = os.path.normpath(os.path.join(SCRIPT_DIR, '..', 'assets', 'maps'))

SOURCE_PNG = os.path.join(MAP_DIR, 'map.png')
MINI_MAP_PNG = os.path.join(MAP_DIR, 'minimap.png')
MANIFEST_PATH = os.path.join(MAP_DIR, 'tile-manifest.json')

# ── Tile config ─────────────────────────────────────────────────
TILE_SIZE = 1024
EDGE_FILL_COLOR = (0, 0, 0, 0)  # Transparent for partial edge tiles

# Quality levels: 100 = lossless, rest are lossy webp quality values
# Matches the 4 tiers in settings: Low (q10), Medium (q70), High (q95), Perfect (q100)
QUALITY_LEVELS = [100, 95, 70, 10]


def fmt_size(num_bytes):
    """Format bytes as a human-readable string."""
    mb = num_bytes / (1024 * 1024)
    if mb >= 1:
        return f"{mb:.1f} MB"
    return f"{num_bytes / 1024:.1f} KB"


def step_banner(step_num, title):
    print()
    print(f"{'=' * 60}")
    print(f"  Step {step_num}: {title}")
    print(f"{'=' * 60}")


def create_mini_map(img):
    """Resize full map to 1000x550 and save as lossless PNG."""

    step_banner(1, "Create minimap.png (1000x550)")

    w, h = img.size
    mini = img.resize((1000, 550), Image.LANCZOS)
    print(f"  Resized: {w}x{h} → {mini.width}x{mini.height}")

    print(f"  Saving {MINI_MAP_PNG} ...")
    mini.save(MINI_MAP_PNG, 'PNG')
    print(f"    → {fmt_size(os.path.getsize(MINI_MAP_PNG))}")

    del mini  # Free memory before heavy steps
    print("  Done with mini map.")


def compute_tile_grid(img_width, img_height):
    """Compute center-origin tile grid bounds."""
    center_px = img_width / 2.0
    center_py = img_height / 2.0

    min_col = math.floor(-center_px / TILE_SIZE)
    max_col = math.floor((img_width - 1 - center_px) / TILE_SIZE)
    min_row = math.floor(-center_py / TILE_SIZE)
    max_row = math.floor((img_height - 1 - center_py) / TILE_SIZE)

    return min_col, max_col, min_row, max_row, center_px, center_py


def extract_tiles(img):
    """Extract all tile crops from the source image into memory.

    Returns a list of (col, row, tile_image) tuples.
    This lets us slice once and save at every quality level without
    re-reading the giant source image each time.
    """
    img_width, img_height = img.size
    min_col, max_col, min_row, max_row, center_px, center_py = \
        compute_tile_grid(img_width, img_height)

    total_tiles = (max_col - min_col + 1) * (max_row - min_row + 1)
    print(f"  Tile grid: cols [{min_col}..{max_col}], rows [{min_row}..{max_row}]")
    print(f"  Maximum tiles: {total_tiles}")

    tiles = []
    for col in range(min_col, max_col + 1):
        for row in range(min_row, max_row + 1):
            world_x = col * TILE_SIZE
            world_y = row * TILE_SIZE

            px_left = int(world_x + center_px)
            px_top = int(world_y + center_py)
            px_right = px_left + TILE_SIZE
            px_bottom = px_top + TILE_SIZE

            src_left = max(0, px_left)
            src_top = max(0, px_top)
            src_right = min(img_width, px_right)
            src_bottom = min(img_height, px_bottom)

            if src_left >= src_right or src_top >= src_bottom:
                continue

            tile_crop = img.crop((src_left, src_top, src_right, src_bottom))

            crop_w = src_right - src_left
            crop_h = src_bottom - src_top
            if crop_w < TILE_SIZE or crop_h < TILE_SIZE:
                canvas = Image.new('RGBA', (TILE_SIZE, TILE_SIZE), EDGE_FILL_COLOR)
                paste_x = src_left - px_left
                paste_y = src_top - px_top
                canvas.paste(tile_crop, (paste_x, paste_y))
                tile_crop = canvas

            tiles.append((col, row, tile_crop))

    print(f"  Extracted {len(tiles)} tiles into memory.")
    return tiles


def save_tiles_at_quality(tiles, quality):
    """Save all tiles to the appropriate tiles_qXX folder."""
    folder_name = f"tiles_q{quality}"
    folder_path = os.path.join(MAP_DIR, folder_name)

    # Clean out old tiles if the folder exists
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    os.makedirs(folder_path, exist_ok=True)

    is_lossless = (quality == 100)
    mode_str = "lossless" if is_lossless else f"quality {quality}"

    total_bytes = 0
    for col, row, tile_img in tiles:
        filename = f"tile_{col}_{row}.webp"
        filepath = os.path.join(folder_path, filename)

        if is_lossless:
            tile_img.save(filepath, 'WEBP', lossless=True)
        else:
            tile_img.save(filepath, 'WEBP', quality=quality)

        total_bytes += os.path.getsize(filepath)

    print(f"    {folder_name:12s}  ({mode_str:12s})  →  {len(tiles)} tiles,  {fmt_size(total_bytes)}")
    return total_bytes


def write_manifest(img_width, img_height):
    """Write tile-manifest.json."""
    min_col, max_col, min_row, max_row, _, _ = \
        compute_tile_grid(img_width, img_height)

    manifest = {
        "tileSize": TILE_SIZE,
        "format": "webp",
        "bounds": {
            "minCol": min_col,
            "maxCol": max_col,
            "minRow": min_row,
            "maxRow": max_row
        },
        "origin": "center",
        "mapPixelWidth": img_width,
        "mapPixelHeight": img_height
    }

    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=4)

    print(f"  Manifest written to {MANIFEST_PATH}")


def main():
    start_time = time.time()

    print(f"{'=' * 60}")
    print(f"  update-map-from-full-map-png.py")
    print(f"  Source: {SOURCE_PNG}")
    print(f"{'=' * 60}")

    # ── Validate source ─────────────────────────────────────────
    if not os.path.isfile(SOURCE_PNG):
        print(f"\n[ERROR] Source file not found: {SOURCE_PNG}")
        print("  Make sure map.png is in assets/maps/")
        sys.exit(1)

    source_size = os.path.getsize(SOURCE_PNG)
    print(f"  Source file size: {fmt_size(source_size)}")

    # ── Load source image ───────────────────────────────────────
    print(f"\n  Loading map.png (this may take a moment) ...")
    img = Image.open(SOURCE_PNG)
    img_width, img_height = img.size
    print(f"  Dimensions: {img_width} x {img_height}")

    if img.mode != 'RGBA':
        img = img.convert('RGBA')
        print(f"  Converted to RGBA")

    # ── Step 1: Mini map ────────────────────────────────────────
    create_mini_map(img)

    # ── Step 2: Extract tiles into memory ───────────────────────
    step_banner(2, "Extract tiles from map.png")
    tiles = extract_tiles(img)

    # ── Step 3: Save tiles at every quality level ───────────────
    step_banner(3, f"Save tiles at {len(QUALITY_LEVELS)} quality levels")
    print()

    grand_total_bytes = 0
    for q in QUALITY_LEVELS:
        total_bytes = save_tiles_at_quality(tiles, q)
        grand_total_bytes += total_bytes

    print(f"\n  Total tile data across all quality levels: {fmt_size(grand_total_bytes)}")

    # ── Step 4: Write manifest ──────────────────────────────────
    step_banner(4, "Write tile-manifest.json")
    write_manifest(img_width, img_height)

    # ── Summary ─────────────────────────────────────────────────
    elapsed = time.time() - start_time
    minutes = int(elapsed // 60)
    seconds = elapsed % 60

    print()
    print(f"{'=' * 60}")
    print(f"  ALL DONE!")
    print(f"{'=' * 60}")
    print(f"  Source:          {img_width} x {img_height} px ({fmt_size(source_size)})")
    print(f"  Mini map:        1000 x 550 px (lossless PNG)")
    print(f"  Tile folders:    {len(QUALITY_LEVELS)} ({', '.join(f'q{q}' for q in QUALITY_LEVELS)})")
    print(f"  Tiles per level: {len(tiles)}")
    print(f"  Total tile data: {fmt_size(grand_total_bytes)}")
    print(f"  Time elapsed:    {minutes}m {seconds:.1f}s")
    print()


if __name__ == '__main__':
    main()
