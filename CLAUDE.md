# Quest Complete Solo

A browser-based incremental RPG/quest adventure game built as a single HTML5 file.

## Project Structure

```
index.html                      — The entire game (HTML + CSS + JS in one file)
scripts/
  update-map-from-full-map-png.py — Generates minimap + tiles from map.png
assets/
  maps/
    map.png                     — Hi-res source map (16384x12288, 351 MB, gitignored)
    map_q100.webp               — Compressed source map (203 MB, gitignored)
    minimap.png                 — Generated 1000x550 minimap (gitignored, regenerate via script)
    tile-manifest.json          — Tile grid metadata
    tiles_q10/                  — Low quality tiles (gitignored)
    tiles_q70/                  — Medium quality tiles (gitignored)
    tiles_q95/                  — High quality tiles (gitignored, default)
    tiles_q100/                 — Perfect/lossless tiles (gitignored)
    testmap.png                 — Legacy map (2048x1536)
    testmap1.png                — Legacy map variant
  icons/
    relic-1.png                 — Relic item icon (1024x1024)
  models/
    test-scene.glb              — 3D test scene (glTF binary)
    hero-friend/                — Character model (Ready Player Me / Prisma3D)
      source/                   — .glb model file
      textures/                 — PBR texture maps (diffuse, normal, metallic)
```

## Game Systems

- **Quest System** — Multi-step quests with dialogue, objectives, and rewards
- **Combat** — Real-time combat with enemy spawning and damage calculations
- **Skill Tree** — Three branches: Damage, Mobility, Utility
- **Merchant/Shop** — Buy and sell relics
- **World Map** — 16384x12288 world with biomes, towns, and fog of war
- **Minimap & Full Map** — Canvas-rendered navigation aids
- **Collection Log** — Track discovered items
- **Dialogue** — Typewriter-style NPC dialogue system

## Tile Map System

The world map uses a tiled rendering system for performance:

- Source `map.png` (16384x12288) is sliced into 1024x1024 WebP tiles at 4 quality levels
- Only tiles visible in the viewport are loaded (typically 6-12 at a time)
- Tiles are cached after first load — no re-fetching
- Quality is switchable in-game via bottom bar buttons (Low/Med/High/Max)
- Default quality is High (q95)
- Tiles overlap by 1px when drawn to prevent seam lines
- Run `python scripts/update-map-from-full-map-png.py` to regenerate tiles from source

## Technical Notes

- The game is a single HTML file by design. Do not split it.
- Assets are referenced via relative paths from the HTML file.
- Rendering uses HTML5 Canvas 2D (three canvases: game, minimap, full map).
- Game loop runs via `requestAnimationFrame`.
- All generated map assets (tiles, minimap) are gitignored. Regenerate with the script.
- Existing game content (biomes, towns, quests) occupies the top-left ~6400x5200 area. The rest of the 16384x12288 world is available for future expansion.
- The 3D character model (`hero-friend/`) is not yet integrated into the game — it's staged for future use.
