# Software Architecture

> Status: draft.

## 1. Module overview

| Module | Owner | Responsibility |
|---|---|---|
| `config/` | Semere | Parse JSON-with-comments config, validate, apply safe defaults |
| `maze/` | | Adapter around the assigned A-Maze-ing package; exposes a stable internal `Maze` representation |
| `engine/` | | Main loop, timestep, rendering entrypoint |
| `entities/` | Lucas | `Player`, `Ghost`, `PacGum`, `SuperPacGum` |
| `scoring/` | | Score tracking + highscore persistence |
| `ui/` | | Main menu, HUD, pause menu, game-over/victory screens |
| `cheat/` | | Cheat mode toggle + feature set |

Each module should only depend on the modules below it in this table where
possible — e.g. `ui/` reads from `scoring/` and `entities/`, but `entities/`
should not import anything from `ui/`.

## 2. Class diagram

```mermaid
classDiagram
    class GameEngine {
        -Config config
        -Maze maze
        -Player player
        -List~Ghost~ ghosts
        -ScoreManager score
        -HighscoreManager highscores
        -CheatMode cheat
        -GameState state
        +run()
        +update(dt)
        +render()
    }

    class ConfigLoader {
        +load(path) Config
        -strip_comments(text) str
        -validate(data) Config
    }

    class Config {
        +int lives
        +int points_per_pacgum
        +int points_per_super_pacgum
        +int points_per_ghost
        +int level_max_time
        +int seed
        +str highscore_filename
        +List~LevelConfig~ levels
    }

    class MazeAdapter {
        +generate(seed, perfect) Maze
    }

    class Maze {
        +Grid walls
        +List~Position~ pacgum_positions
        +List~Position~ super_pacgum_positions
        +List~Position~ ghost_corners
        +Position player_start
    }

    class Player {
        -Position position
        -int lives
        -bool invincible
        +move(direction)
        +eat_pacgum()
        +eat_super_pacgum()
        +lose_life()
        +respawn()
    }

    class Ghost {
        -Position position
        -GhostState state
        -Corner home_corner
        +update(dt, player_pos)
        +become_edible()
        +get_eaten()
        +respawn()
    }

    class GhostState {
        <<enumeration>>
        CHASE
        EDIBLE
        EATEN
    }

    class ScoreManager {
        -int score
        +add_pacgum()
        +add_super_pacgum()
        +add_ghost()
        +get_score() int
    }

    class HighscoreManager {
        -str filename
        -List~HighscoreEntry~ entries
        +load()
        +save()
        +add_entry(name, score)
        +top(n) List~HighscoreEntry~
    }

    class CheatMode {
        -bool active
        +toggle_invincibility()
        +skip_level()
        +freeze_ghosts()
        +add_lives()
        +boost_speed()
    }

    class UIManager {
        +show_main_menu()
        +show_hud()
        +show_pause_menu()
        +show_game_over(score)
        +show_victory(score)
    }

    GameEngine --> ConfigLoader
    GameEngine --> MazeAdapter
    GameEngine --> Player
    GameEngine --> Ghost
    GameEngine --> ScoreManager
    GameEngine --> HighscoreManager
    GameEngine --> CheatMode
    GameEngine --> UIManager
    ConfigLoader --> Config
    MazeAdapter --> Maze
    Ghost --> GhostState
```

## 3. Design notes / open decisions

- **Ghost behavior strategy**: consider a `Strategy` pattern so `chase`,
  `flee`, and `eaten` movement logic are swappable per-ghost rather than
  branching inside `Ghost.update()`. Not required, but keeps `GHO-02`/`GHO-03`
  testable in isolation.
- **`MazeAdapter` boundary**: this is the one class allowed to know about the
  external A-Maze-ing package's actual interface (per subject V.4 — "your
  loader must adapt to their interface"). Nothing else in the codebase should
  import that package directly — route everything through `MazeAdapter` so a
  package API change only touches one file.
- **Config immutability**: once loaded, treat `Config` as read-only for the
  rest of the run — avoids accidental state bugs from something mutating
  config mid-game.

## 4. Why this shape

Rough justification for anyone reading this cold (or for defense purposes):
`GameEngine` is the only class that knows about everything else — every other
class is testable independently without spinning up the full engine, which is
what `TEST-01`'s unit tests rely on.
