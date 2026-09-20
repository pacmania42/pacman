# Analysis, choices and risks

## Technical choices

| Decision | Alternative | Why |
|---|---|---|
| Scene stack (`SceneStack`) | one big state machine in the game loop | pause has to draw the gameplay behind it; a stack gives that for free, and every screen becomes independent |
| `GameState` holds no drawing code | entities draw themselves | it was the seam between the two of us (see [team-organization.md](team-organization.md)); it also makes the logic testable without a window |
| pydantic for config **and** highscore | hand-written validation | the subject demands clamping to defaults with clear messages and no traceback; pydantic gives per-field validators and a typed model for free, and we already needed it once |
| Grid-based movement between cell centres | free pixel movement with wall collision | actors can only ever follow corridor links, so walking through a wall is unrepresentable rather than merely prevented |
| Own bitmap-font `string_put` | drop text, or another graphics library | MLX has no text output and the subject restricts us to MLX-equivalent functions |
| uv + `wheels/` for the assigned package | pip + requirements.txt | the maze package is a local wheel that gets re-installed at review; pinning it in `pyproject.toml` makes that one command |

## Risks and mitigation

| Risk | Impact | Mitigation | Outcome |
|---|---|---|---|
| The assigned A-Maze-ing package is re-installed at review and behaves differently | maze generation breaks at defense | wrapper isolates the package in `src/entities/maze.py`; nothing else calls it | held, the wrapper is the only call site |
| Two people editing the same files | constant conflicts, lost work | split along simulation/presentation, enforced by issue ownership | held |
| MLX is thin and undocumented | unknown unknowns late in the project | spiked the maze and the window early (W36) | partly held, the missing text output was found late enough to cost a day (`utils-00`) |
| Bad config crashes the game at review | subject treats a traceback as non-functional | clamp-and-continue loader, a unit test per malformed-input case | held |

## Blocking points

- **MLX has no text rendering.** Found when the first screen needed a score.
  Blocked all UI work until a bitmap-font renderer existed (`UTILS-00`, one
  day). This is the single largest unplanned item in the project.
- **Respawn and movement alignment** (`BUG-03`). Actors drifted off the grid
  and respawned in the wrong cell, which only showed up once sprites replaced
  placeholder rectangles. Fixed by consolidating respawn into one place.

No conflicts between the two of us worth recording, the area split meant we
rarely had a reason to disagree about the same file. The handful of reviews
that asked for changes were all resolved on the branch.
