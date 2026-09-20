# Acceptance test plan

Two layers: automated checks that run on every push, and a manual pass before
a release build.

## Automated

[CI](../.github/workflows/ci.yml) runs on every push to `main` and every pull
request, in two jobs:

| Job | Command | Covers |
|---|---|---|
| lint | `make lint` | ruff, flake8, and mypy with the flags the subject mandates |
| test | `make test` | the pytest suite |

`make lint-strict` runs the same with `mypy --strict`; the code passes that
too, but the subject only requires the flag set in `lint`.

The suite concentrates on the config loader, because that is where the
subject is strictest, malformed input must never produce a traceback:

- valid config, valid top-level array, comment-only file
- missing file, malformed JSON, non-dict JSON, non-dict level entries
- unknown keys ignored, missing optional keys defaulted
- invalid field values clamped, `levels` minimum length enforced
- comment stripping
- one test for the input event sink

Game logic is not unit-tested. It is exercised manually (below), which is the
main gap in this plan.

Beyond the two CI jobs, every change to `main` also passed a human check, see
[team-organization.md](team-organization.md#reviews).

## Manual pass

Run before tagging a build with `make run`:

| Area | Check |
|---|---|
| Main menu | Start, Instructions, Highscore, Exit all reachable; ESC quits |
| Gameplay | movement on arrows and WASD; no wall crossing; dots and pellets score |
| Ghosts | chase when normal, flee when frightened, respawn in their corner |
| HUD | score, lives, current level, remaining time all update |
| Pause | P pauses, resume and main-menu both work |
| Level end | clearing all dots advances; score and lives carry over |
| Game over | lives at zero and timer at zero both end the game |
| Victory | clearing the last level shows the victory screen |
| Highscore | name entry accepts ≤10 alphanumerics; table persists across runs |
| Config | a deliberately broken config prints messages and still starts |
| Package | built binary launches and plays |
