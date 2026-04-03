# Quest Complete Solo — Quest Creation Prompt

Use this prompt when asking Claude to generate new quests for the game.

---

## Prompt Template

Copy and paste the following into Claude, filling in the bracketed sections:

---

You are a quest designer for "Quest Complete Solo", a browser-based incremental RPG. Generate a quest JSON object following the exact schema below.

### World Context

The game world is 16384x12288 pixels with these biomes and towns:

**Biomes:**
- Greenhollow Plains (0,0 to 2200,2600) — peaceful farmland
- Darkwood Forest (2200,0 to 4200,2000) — dangerous woods
- Ashfall Wastes (4200,0 to 6400,2600) — volcanic wasteland
- Crystal Lake (0,2600 to 2600,5200) — lakeside region
- Ironpeak Mountains (2600,2000 to 4400,3800) — rugged peaks
- Sunscorch Desert (4200,2600 to 6400,5200) — arid desert
- The Shadowmere (2600,3800 to 4200,5200) — dark realm

**Existing Towns (can be referenced by node ID):**
- willowbrook (900, 2600) — starting village
- thornwatch (700, 1200) — frontier outpost
- eldergrove (3000, 800) — druid settlement
- cinderhold (5000, 1200) — dwarven forge
- mistport (900, 3900) — port town
- ironhaven (3400, 2800) — mountain city
- sunspire (5400, 3600) — sun elf city
- shadowmere-sanctum (3400, 4400) — hidden monastery
- briarwood (1800, 1600) — logging camp
- dusthaven (4600, 2200) — desert post
- frostmere (1200, 600) — fishing hamlet
- stonekeep (3000, 2200) — mountain fortress
- ashfall-camp (4800, 600) — scavenger settlement
- lakeside (1600, 3200) — lakeside village
- duskhollow (2800, 4800) — shadowmere outpost

**Enemy Types (use exact names):**
- Slime (Lv1), Wolf (Lv2), Bandit (Lv3), Forest Spirit (Lv3)
- Bone Archer (Lv4), Cave Troll (Lv5), Dark Knight (Lv6)
- Sand Wyrm (Lv7), Shadow Wraith (Lv8), Fire Elemental (Lv9)
- Wraith Lord (Lv10), Dragon Whelp (Lv11)

### Quest JSON Schema

```json
{
  "id": "unique_id",
  "name": "Quest Name",
  "type": "M|S|B|G",
  "chapter": 0,
  "description": "Short description shown in quest list.",
  "levelReq": 1,
  "steps": [
    {
      "type": "dlg|travel|discover|combat",
      "node": "existing-node-id or null",
      "text": "Step display text",
      "enemy": null,
      "count": 0
    }
  ],
  "rewards": {"xp": 100, "gold": 50},
  "lore": "Lore text shown on completion.",
  "unlocks": ["quest-id-1", "quest-id-2"],
  "dialogue": [
    {"speaker": "NPC Name", "text": "What the NPC says."}
  ],
  "newNodes": [
    {
      "id": "new-node-id",
      "name": "Display Name",
      "type": "poi",
      "radius": 45,
      "description": "What this place is."
    }
  ]
}
```

### Step Types

| Type | Description | Required Fields |
|------|-------------|-----------------|
| `dlg` | Show next dialogue line | Just `type` and `text` |
| `travel` | Move to a location | `node` (existing or new node ID) |
| `discover` | Travel + mark town as discovered | `node` (must be a town node) |
| `combat` | Fight enemies at current location | `enemy` (exact name), `count` |

### Rules

1. **Quest types**: M = Main story, S = Side quest, B = Bounty (combat-focused), G = Gather (travel-focused)
2. **Every quest starts and ends with `dlg`** — opening dialogue and closing dialogue
3. **Dialogue array length** must match the number of `dlg` steps
4. **Combat steps don't need a node** — enemies spawn at the player's current position
5. **`newNodes`** — list any NEW locations this quest needs that don't exist yet. The designer will position them in the editor. Set x/y to 0,0 as placeholder.
6. **`node: null`** on travel/discover steps means the designer needs to place this in the editor
7. **Level requirements** should match enemy difficulty (Slime=1, Wolf=2, Bandit=3, etc.)
8. **Rewards scale**: ~40xp/25g at Lv1, scaling up to ~1000xp/500g at Lv12
9. **`unlocks`** — quest IDs that become available after completing this quest. Leave empty `[]` if none.
10. **Lore** — 1-2 sentences of world-building revealed on completion

### My Quest Request

[Describe what kind of quest you want here. Include:]
- Theme/story premise
- Approximate level range
- Which region of the world
- Quest type (Main/Side/Bounty/Gather)
- Any specific NPCs or enemies to include
- How many steps (short: 3-5, medium: 5-8, long: 8-12)

---

## Example Output

Here's what a properly formatted quest looks like:

```json
{
  "id": "s20",
  "name": "The Hollow Tree",
  "type": "S",
  "chapter": 0,
  "description": "Investigate strange noises from the old hollow tree.",
  "levelReq": 3,
  "steps": [
    {"type": "dlg", "text": "Speak with Ranger Wynn"},
    {"type": "travel", "node": "hollow-tree", "text": "Find the hollow tree"},
    {"type": "combat", "text": "Clear the nest", "enemy": "Wolf", "count": 4},
    {"type": "travel", "node": "briarwood", "text": "Return to Briarwood"},
    {"type": "dlg", "text": "Report to Ranger Wynn"}
  ],
  "rewards": {"xp": 85, "gold": 42},
  "lore": "The wolves had been nesting in the tree's roots, driven there by something deeper in the forest.",
  "unlocks": [],
  "dialogue": [
    {"speaker": "Ranger Wynn", "text": "Something's howling from the old hollow tree east of camp. Sounds like a whole pack moved in."},
    {"speaker": "Ranger Wynn", "text": "A wolf den in the roots! No wonder they were so aggressive. Good work clearing them out."}
  ],
  "newNodes": [
    {
      "id": "hollow-tree",
      "name": "Hollow Tree",
      "type": "poi",
      "radius": 45,
      "description": "An ancient hollow tree east of Briarwood."
    }
  ]
}
```

## After Getting the JSON

1. Copy the quest JSON output
2. Open the Quest Editor (`editor.html`)
3. Click "Import Quest" and paste the JSON
4. New nodes will appear on the map at placeholder positions — drag them to proper locations
5. Existing node references will snap to their correct positions automatically
6. Click "Export" to save the updated quests.json and nodes.json
