from enum import Enum, auto

class CellState(Enum):
    HIDDEN = auto()
    REVEALED = auto()
    FLAGGED = auto()