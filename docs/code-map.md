# Code map

The game is a window driving a stack of screens. `Game` runs the
loop and owns the `SceneStack`; every screen is a `Scene`.
`GameplayScene` is the only one with a simulation behind it: it
owns a `GameState`, which holds the `Maze`, the `Player`, the
ghosts and the dots, and a `GameView` that draws them.

Everything the player can eat derives from `Edible`, everything
that moves from `Actor`. `GameState` never draws, and no entity
knows a scene exists.

Only the classes that carry the structure are shown. Enums,
exceptions, pydantic models and small value types are left out.

```mermaid
classDiagram
    direction LR
    %% src
    class Game
    class GameState
    %% src/core
    class Scene
    class SceneStack
    %% src/entities
    class Actor
    class Edible
    class Ghost
    class Maze
    class Pacgum
    class Player
    class SuperPacgum
    %% src/scenes
    class GameOverScene
    class GameplayScene
    class HighScoreScene
    class InstructionsScene
    class MenuScene
    class PauseScene
    %% src/ui
    class GameView
    Edible <|-- Actor
    Scene <|-- GameOverScene
    Scene <|-- GameplayScene
    Actor <|-- Ghost
    Scene <|-- HighScoreScene
    Scene <|-- InstructionsScene
    Scene <|-- MenuScene
    Edible <|-- Pacgum
    Scene <|-- PauseScene
    Actor <|-- Player
    Pacgum <|-- SuperPacgum
    Game --> SceneStack
    GameState --> Ghost
    GameState --> Maze
    GameState --> Pacgum
    GameState --> Player
    GameState --> SuperPacgum
    GameplayScene --> GameState
    GameplayScene --> GameView
    Ghost --> Maze
    Player --> Maze
```
