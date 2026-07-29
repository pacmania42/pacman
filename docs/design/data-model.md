# Data Model

> Status: draft.

## 1. Config file schema

Suggested structure (subject V.2 says exact structure is up to you — this is
a starting proposal, adjust as needed):

```jsonc
{
  // Lines starting with # are comments and are stripped before parsing
  "highscore_filename": "highscores.json",
  "lives": 3,
  "pacgum": 42,
  "points_per_pacgum": 10,
  "points_per_super_pacgum": 50,
  "points_per_ghost": 200,
  "seed": 42,
  "level_max_time": 90,
  "levels": [
    { "width": 21, "height": 21 },
    { "width": 25, "height": 25 }
  ]
}
```

| Key | Type | Default (if missing/invalid) | Notes |
|---|---|---|---|
| `highscore_filename` | str | `"highscores.json"` | relative to project root |
| `lives` | int > 0 | `3` | |
| `pacgum` | int >= 0 | `42` | count target, may be derived from maze instead |
| `points_per_pacgum` | int >= 0 | `10` | |
| `points_per_super_pacgum` | int >= 0 | `50` | |
| `points_per_ghost` | int >= 0 | `200` | |
| `seed` | int | `42` | used for level 1 only; later levels randomize |
| `level_max_time` | int seconds > 0 | `90` | |
| `levels` | list of `{width, height}` | single default level | at least 10 required at runtime (subject VI.7) — can repeat/cycle a shorter config list if fewer than 10 are specified, document whichever approach is chosen |

**Unknown keys**: ignored, not an error (subject V.3).
**Invalid values** (wrong type, negative where positive required, etc.):
clamp to the default above, log a message, continue — never raise.

## 2. Highscore file schema

```jsonc
{
  "entries": [
    { "name": "Sannaka", "score": 1110 },
    { "name": "foliole", "score": 20 },
    { "name": "Marmelade", "score": 20 }
  ]
}
```

| Field | Type | Constraint |
|---|---|---|
| `name` | str | max 10 chars, alphanumeric + spaces only |
| `score` | int | non-negative |

Rules:
- Keep only the **top 10** entries, sorted descending by score.
- On missing file: treat as empty list, create fresh on first save.
- On corrupt/unparseable file: log a warning, fall back to empty list rather
  than crashing (subject V.5).
- Write is a full-file rewrite (load → append/sort/trim → save), not an
  incremental append — simpler and avoids partial-write corruption at this
  project's scale.

## 3. Runtime (non-persisted) data

Not saved to disk, but worth naming here since they're shared across
modules and easy to accidentally duplicate state for:

- **Current score** — lives in `ScoreManager` for the run; only touches
  `HighscoreManager` at game-over/victory.
- **Current level index** — lives in `GameEngine`; resets maze via
  `MazeAdapter` on transition, does not reset score/lives.
- **Cheat mode flags** — lives in `CheatMode`, never persisted, resets each
  run (cheat state shouldn't carry into a fresh `python3 pac-man.py ...`).
