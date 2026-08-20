# mazegenerator API

### Pydoc documentation (enhanced)
```manpage
Help on package mazegenerator:

NAME
    mazegenerator

PACKAGE CONTENTS
    mazegenerator

CLASSES
    builtins.object
        mazegenerator.mazegenerator.MazeGenerator

    class MazeGenerator(builtins.object)
     |  MazeGenerator(
     |      size: tuple[int, int] = (15, 15),
     |      perfect: bool = False,
     |      entry_cell: tuple[int, int] = (0, 0),
     |      exit_cell: tuple[int, int] = (-1, -1),
     |      seed: int = 0
     |  ) -> None
     |
     |  Methods defined here:
     |
     |  __init__(
     |      self,
     |      size: tuple[int, int] = (15, 15),
     |      perfect: bool = False,
     |      entry_cell: tuple[int, int] = (0, 0),
     |      exit_cell: tuple[int, int] = (-1, -1),
     |      seed: int = 0
     |  ) -> None
     |      Initialize self.  See help(type(self)) for accurate signature.
     |
     |  generate(self, seed: int = 0) -> None
     |
     |  ----------------------------------------------------------------------
     |  Readonly properties defined here:
     |
     |  maze: list[list[int]]
     |
     |  maze_entry: tuple[int, int]
     |
     |  maze_exit: tuple[int, int]
     |
     |  shortest_path: str
     |
     |  ----------------------------------------------------------------------
     |  Data descriptors defined here:
     |
     |  __dict__
     |      dictionary for instance variables
     |
     |  __weakref__
     |      list of weak references to the object

DATA
    __all__ = ['MazeGenerator']

FILE
    /home/semere/projects/42/pacman/.venv/lib/python3.13/site-packages/mazegenerator/__init__.py


  
```


### Usage

```python
>>> from mazegenerator.mazegenerator import MazeGenerator
>>> gen = MazeGenerator()
>>> [member for member in dir(gen) if not member.startswith("_")]
['generate', 'maze', 'maze_entry', 'maze_exit', 'shortest_path']
>>> gen.maze
[[9, 3, 9, 1, 1, 5, 5, 1, 1, 5, 5, 1, 1, 5, 3], [10, 12, 2, 10, 12, 5, 1, 2, 8, 5, 1, 6, 8, 1, 2], [8, 1, 6, 8, 5, 5, 2, 12, 4, 1, 4, 5, 4, 2, 10], [10, 12, 5, 6, 9, 5, 4, 5, 3, 8, 1, 1, 1, 6, 10], [12, 1, 1, 3, 12, 1, 5, 1, 4, 6, 12, 2, 8, 1, 2], [9, 2, 8, 6, 15, 8, 3, 10, 15, 15, 15, 8, 6, 12, 2], [10, 12, 0, 3, 15, 12, 4, 0, 5, 7, 15, 8, 5,3, 10], [8, 1, 2, 10, 15, 15, 15, 10, 15, 15, 15, 12, 1, 2, 10], [8, 6, 8, 4, 5, 3, 15, 10, 15, 13, 5, 1, 2, 10, 10], [10, 9, 0, 3, 9, 2, 15, 10, 15, 15, 15, 10, 12, 2, 10], [10, 12, 6, 10, 12, 6, 9, 4, 1, 3, 9, 0, 5, 4, 2], [8, 1, 3, 12, 3, 9, 4, 1, 2, 10, 10, 8, 1, 5, 2], [8, 2, 8, 1, 2, 8, 3, 8, 4, 4, 0, 6, 12, 5, 2], [10, 10, 8, 2, 8, 2, 12, 4, 5, 1, 0, 3, 9, 3, 10], [12, 4, 4, 4, 4, 4, 5, 5, 5, 4, 6, 12, 6, 12, 6]]
>>> gen.maze_entry
(0, 0)
>>> gen.maze_exit
(14, 14)
>>> gen.shortest_path
'ESENEEEEEEEEEEEESSSSSSSSSSSSSS'
>>>
  
```
