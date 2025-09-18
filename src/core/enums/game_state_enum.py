from enum import Enum, auto

class GameStateEnum(Enum):
    READY = auto()      # Game hasn't started, waiting for first click
    RUNNING = auto()    # Game is in progress
    WON = auto()        # All non-mine cells revealed
    LOST = auto()       # A mine was revealed
