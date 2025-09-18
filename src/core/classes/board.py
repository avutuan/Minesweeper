import random
from core.classes.cell import Cell
from core.enums.cell_state_enum import CellState

class Board:
    """Holds the grid of cells and implements core game logic."""
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

    def _get_neighbors(self, r, c):
        """Returns valid neighbor coordinates for a given cell."""
        neighbors = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    neighbors.append((nr, nc))
        return neighbors

    def place_mines(self, safe_cell_r, safe_cell_c):
        """Places mines randomly, avoiding the first-clicked safe cell."""
        mine_positions = set()
        while len(mine_positions) < self.num_mines:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (r, c) != (safe_cell_r, safe_cell_c):
                mine_positions.add((r, c))

        for r, c in mine_positions:
            self.grid[r][c].has_mine = True

        self._calculate_adjacent_counts()

    def _calculate_adjacent_counts(self):
        """Calculates the number of adjacent mines for each cell."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c].has_mine:
                    continue
                count = 0
                for nr, nc in self._get_neighbors(r, c):
                    if self.grid[nr][nc].has_mine:
                        count += 1
                self.grid[r][c].adjacent_count = count

    def reveal(self, r, c):
        """Reveals a cell and flood-fills if it's a zero."""
        cell = self.grid[r][c]
        if cell.state != CellState.HIDDEN:
            return

        cell.state = CellState.REVEALED

        if cell.has_mine:
            # Game over is handled by the main loop, not the board itself
            return

        # Flood fill for cells with 0 adjacent mines
        if cell.adjacent_count == 0:
            for nr, nc in self._get_neighbors(r, c):
                self.reveal(nr, nc)

    def toggle_flag(self, r, c):
        """Toggles a flag on a hidden cell."""
        cell = self.grid[r][c]
        if cell.state == CellState.HIDDEN:
            cell.state = CellState.FLAGGED
        elif cell.state == CellState.FLAGGED:
            cell.state = CellState.HIDDEN

    def is_cleared(self):
        """Checks if all non-mine cells have been revealed."""
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                if not cell.has_mine and cell.state != CellState.REVEALED:
                    return False
        return True