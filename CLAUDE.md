# Quest Complete Solo

A browser-based incremental RPG/quest adventure game built as a single HTML5 file.

## Project Structure

```
index.html                      — The entire game (HTML + CSS + JS in one file)
assets/
  maps/
    testmap.png                 — World map (2048x1536, 6.1 MB)
    testmap1.png                — World map variant (2048x1536, used in-game)
    map.png                     — Hi-res world map (16384x12288, 351 MB, gitignored)
    map_q100.webp               — Compressed hi-res map (203 MB, gitignored)
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
- **World Map** — 6400x5200 world with biomes, towns, and fog of war
- **Minimap & Full Map** — Canvas-rendered navigation aids
- **Collection Log** — Track discovered items
- **Dialogue** — Typewriter-style NPC dialogue system

## Technical Notes

- The game is a single HTML file by design. Do not split it.
- Assets are referenced via relative paths from the HTML file (e.g. `assets/maps/testmap1.png`).
- Rendering uses HTML5 Canvas 2D (three canvases: game, minimap, full map).
- Game loop runs via `requestAnimationFrame`.
- The large map files (`map.png`, `map_q100.webp`) are gitignored due to size. They are reference/source art for the world.
- The 3D character model (`hero-friend/`) is not yet integrated into the game — it's staged for future use.
