# Timeline and progress

Three weeks, 3–20 September 2026 on
[pacmania42/pacman](https://github.com/pacmania42/pacman).

## Plan

We split the subject into epics and gave each a short prefix, used in issue
titles, branch names and commit messages. Work was pulled from the top of the
board's Ready column, so the plan below is the order we intended, not fixed
dates.

```mermaid
gantt
    title Pac-Man, planned vs actual
    dateFormat YYYY-MM-DD
    axisFormat %d %b

    section Foundations
    Setup, tooling, CI (stp)        :2026-09-03, 3d
    Maze package spike (maze)       :2026-09-05, 1d
    Config loader (cfg)             :2026-09-06, 3d

    section Engine
    Game class, scenes, input (gam) :2026-09-05, 9d
    Actors and movement (act)       :2026-09-08, 4d
    Collision detection (gam-03)    :2026-09-12, 2d

    section Presentation
    Screens and menus (ui)          :2026-09-05, 13d
    Own string_put (utils)          :2026-09-11, 1d
    Highscore system (his)          :2026-09-13, 2d
    Sprites and animation (sprites) :2026-09-13, 6d
    HUD (hud)                       :2026-09-17, 1d

    section Delivery
    Level progression (game-04)     :2026-09-19, 2d
    Cheat mode (cht)                :2026-09-20, 1d
    Packaging to itch.io (dpl)      :2026-09-20, 1d
    README and docs (doc)           :2026-09-20, 2d
```

## What actually happened

| Week | Planned | Delivered |
|---|---|---|
| W36 (3–6 Sep) | tooling, maze spike, config | all three, plus the first menu screen and the game-state skeleton |
| W37 (7–13 Sep) | actors, collision, first sprites | done; `UTILS-00` (own `string_put`) was added mid-week once we found MLX had no text output |
| W38 (14–20 Sep) | screens, HUD, progression, packaging | done, but compressed: most of the project's work falls in this week |

## Throughput

The board's Done column moved steadily: work was reviewed
each evening. The largest bursts was mid-week three, when most of the
presentation layer landed together.

### Where we drifted

- **Back-loaded.** More than half the work landed in the last week. The engine
  took longer than planned, so progression, cheat mode and packaging were all
  finished in the final two days.
- **`UTILS-00` was unplanned.** MLX has no text drawing, so we had to write a
  bitmap-font renderer before any screen could show a score. One day, not in
  the original plan.
- **Bug epics were not planned at all.** The `BUG` tickets were opened
  reactively.
- **Late tickets** are deployment, documentation and the final fixes. They are the tail of the
  back-loading above, not forgotten work.
