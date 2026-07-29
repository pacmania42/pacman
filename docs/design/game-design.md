# Game Design Notes

> Status: draft.

## 1. Ghost chase behavior (subject VI.3: "up to you")

- **Greedy distance minimization** — at each junction, pick the neighbor
  tile that minimizes straight-line (or Manhattan) distance to the player.
  Simple, looks reasonably intelligent, cheap to compute every frame.

## 2. Ghost flee behavior (when edible)

- **Random Walk**- more defensible here — real Pac-Man ghosts flee
somewhat erratically, so it doesn't need to be as "smart" as chase.

## 3. Level time-out behavior (subject VI.7: "up to you")

- **Restart the level** (same maze, pacguns reset, lives/score kept) — gentler,
  keeps playtesting/evaluation shorter per level.

## 4. Cheat mode specifics (subject VI.5)

| Feature | Suggested key | Notes |
|---|---|---|
| Toggle cheat mode | `` ` `` (backtick) | shown/logged in HUD when active |
| Invincibility | `I` | ghosts pass through player, no life lost |
| Level skip | `N` | immediately triggers level-complete |
| Ghost freeze | `F` | toggles ghosts' `update()` no-op |
| Extra life | `L` | +1 life, no cap needed |
| Speed boost | `+` / `-` | multiplies player move speed |

## 5. Corner assignment (4 ghosts, 4 corners)

```
Top-left     -> Ghost 0
Top-right    -> Ghost 1
Bottom-left  -> Ghost 2
Bottom-right -> Ghost 3
```

## 6. Timing constants (tune during playtesting, record final values here)

| Constant | Suggested starting value | Where used |
|---|---|---|
| Super-pacgum edible duration | 8s | `GHO-03` |
| Eaten-ghost respawn delay | 6s | `GHO-04` |
| Player move speed | TBD, tune to maze cell size | `PLR-01` |
| Ghost move speed (chase) | slightly slower than player | `GHO-02` |
| Ghost move speed (edible/fleeing) | slower still | `GHO-03` |
