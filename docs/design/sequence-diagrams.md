# Sequence Diagrams

> Status: draft.

## 1. Startup sequence

```mermaid
sequenceDiagram
    participant CLI
    participant ConfigLoader
    participant MazeAdapter
    participant HighscoreManager
    participant GameEngine
    participant UIManager

    CLI->>ConfigLoader: load(config.json)
    ConfigLoader-->>CLI: Config (defaults applied where needed, warnings logged)
    CLI->>HighscoreManager: load(highscore_filename)
    HighscoreManager-->>CLI: highscore entries (empty list if file missing/corrupt)
    CLI->>GameEngine: init(config, highscores)
    GameEngine->>MazeAdapter: generate(seed=42, perfect=False)
    MazeAdapter-->>GameEngine: Maze
    GameEngine->>UIManager: show_main_menu()
```

Relevant tickets: `CFG-01`–`CFG-03`, `MAZE-02`–`MAZE-03`, `UI-01`.

## 2. Eating a super-pacgum

```mermaid
sequenceDiagram
    participant Player
    participant Maze
    participant GameEngine
    participant Ghost

    Player->>Maze: check_tile(position)
    Maze-->>Player: SuperPacgum found
    Player->>Player: eat_super_pacgum() [+score]
    Player->>GameEngine: notify(super_pacgum_eaten)
    GameEngine->>Ghost: become_edible()  (broadcast to all ghosts)
    Ghost->>Ghost: start edible timer
    Note over Ghost: timer expires
    Ghost->>Ghost: revert to Chase
```

Relevant tickets: `PLR-02`, `GHO-03`.

## 3. Level transition

```mermaid
sequenceDiagram
    participant GameEngine
    participant Player
    participant MazeAdapter
    participant UIManager

    Player->>GameEngine: notify(all_pacgums_eaten)
    GameEngine->>GameEngine: check current level vs total levels
    alt more levels remain
        GameEngine->>MazeAdapter: generate(random_seed, perfect=False)
        MazeAdapter-->>GameEngine: new Maze
        GameEngine->>Player: reset position to maze center (keep score/lives)
        GameEngine->>UIManager: update HUD (level number)
    else last level complete
        GameEngine->>UIManager: show_victory(score)
    end
```

Relevant tickets: `PROG-01`, `PROG-02`.

## 4. Game over / highscore save

```mermaid
sequenceDiagram
    participant Player
    participant GameEngine
    participant UIManager
    participant HighscoreManager
    participant Disk

    Player->>GameEngine: lose_life() [lives now 0]
    GameEngine->>UIManager: show_game_over(score)
    UIManager->>UIManager: prompt name entry (validate: <=10 chars, alphanumeric+spaces)
    UIManager->>HighscoreManager: add_entry(name, score)
    HighscoreManager->>HighscoreManager: sort + trim to top 10
    HighscoreManager->>Disk: save(highscore_filename)
    UIManager->>UIManager: return to MainMenu
```

Relevant tickets: `SCORE-02`–`SCORE-04`, `UI-04`.

## 5. Maze generator failure (error path)

```mermaid
sequenceDiagram
    participant GameEngine
    participant MazeAdapter
    participant ExternalPackage
    participant UIManager

    GameEngine->>MazeAdapter: generate(seed, perfect=False)
    MazeAdapter->>ExternalPackage: call generator function
    ExternalPackage--xMazeAdapter: raises exception
    MazeAdapter->>MazeAdapter: catch, log clear error message
    MazeAdapter-->>GameEngine: raise MazeGenerationError (typed, not raw exception)
    GameEngine->>UIManager: show error message, return to MainMenu
    Note over GameEngine: never propagates raw traceback (subject III.1 / V.1)
```

Relevant tickets: `MAZE-04`.
