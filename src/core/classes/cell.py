from core.enums.cell_state_enum import CellState

class Cell:
    """Represents a single cell on the board."""
    def __init__(self):
        self.has_mine = False
        self.adjacent_count = 0
        self.state = CellState.HIDDEN