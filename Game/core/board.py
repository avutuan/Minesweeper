"""
Module: board.py
Description: Implements the Minesweeper board, including mine placement, cell management, and win/loss logic.
Author: Tuan Vu
Creation Date: September 14, 2025
External Sources: N/A - Original Code
"""
import random
from core.cell import Cell

class Board:
    """
    Description: Manages the Minesweeper game board including mine placement, cell management, and win/loss logic.
    Author: Tuan Vu
    Creation Date: September 14, 2025
    External Sources: N/A - Original Code
    """
    
    def __init__(self, mine_count=10):
        """
        Description: Initialize a new 10x10 Minesweeper board and set up cell grid and mine count.
        Args:
            mine_count (int): Number of mines to place (10-20, default 10)
        Returns: None
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - board configuration
        self.ROWS = 10
        self.COLS = 10
        self.mine_count = max(10, min(20, mine_count))  # Ensure mine count is between 10-20
        self.first_click = True  # Track if this is the first click
        
        # Initialize 2D grid of Cell objects
        self.grid = [[Cell(row, col) for col in range(self.COLS)] for row in range(self.ROWS)]
        
        # Track game statistics
        self.revealed_cells = 0
        self.total_safe_cells = self.ROWS * self.COLS - self.mine_count
    
    def place_mines(self, safe_row, safe_col):
        """
        Description: Randomly place mines on the board, avoiding the first clicked cell and its neighbors.
        Args:
            safe_row (int): Row of first clicked cell (0-9)
            safe_col (int): Column of first clicked cell (0-9)
        Returns: None
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - random mine placement with safe zone
        # Create list of safe cells (first clicked cell and all adjacent cells)
        safe_cells = set()
        # Mark the first clicked cell and its neighbors as safe.
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                new_row, new_col = safe_row + dr, safe_col + dc
                if 0 <= new_row < self.ROWS and 0 <= new_col < self.COLS:
                    safe_cells.add((new_row, new_col))
        
        mines_placed = 0
        # Place mines randomly, avoiding safe cells and already mined cells.
        while mines_placed < self.mine_count:
            row = random.randint(0, self.ROWS - 1)
            col = random.randint(0, self.COLS - 1)
            if (row, col) in safe_cells or self.grid[row][col].is_mine:
                continue
            self.grid[row][col].set_mine()
            mines_placed += 1
        
        # Calculate adjacent mine counts for all cells
        # After placing mines, calculate adjacent mine counts for all cells.
        self._calculate_adjacent_mines()
    
    def _calculate_adjacent_mines(self):
        """
        Description: Calculate the number of adjacent mines for each cell.
        Args: None
        Returns: None
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - adjacent mine calculation
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if not self.grid[row][col].is_mine:
                    count = self._count_adjacent_mines(row, col)
                    self.grid[row][col].set_adjacent_mines(count)
    
    def _count_adjacent_mines(self, row, col):
        """
        Description: Count mines in the 8 cells adjacent to the given position.
        Args:
            row (int): Row position (0-9)
            col (int): Column position (0-9)
        Returns: int - Number of adjacent mines (0-8)
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - count mines in 3x3 grid around cell
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:  # Skip the cell itself
                    continue
                
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < self.ROWS and 
                    0 <= new_col < self.COLS and 
                    self.grid[new_row][new_col].is_mine):
                    count += 1
        
        return count
    
    def reveal_cell(self, row, col):
        """
        Description: Reveal a cell and potentially trigger recursive revealing of adjacent cells.
        Args:
            row (int): Row position (0-9)
            col (int): Column position (0-9)
        Returns: bool - True if mine was hit (game over), False otherwise
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - cell revealing logic
        if not (0 <= row < self.ROWS and 0 <= col < self.COLS):
            return False
        
        cell = self.grid[row][col]
        
        # Handle first click - place mines after first click to ensure safety
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False
        
        # Cannot reveal flagged or already revealed cells
        if cell.is_flagged or cell.is_revealed:
            return False
        
        # Reveal the cell
        cell.reveal()
        self.revealed_cells += 1
        
        # Check if mine was hit
        if cell.is_mine:
            return True  # Game over
        
        # If cell has no adjacent mines, recursively reveal adjacent cells
        if cell.adjacent_mines == 0:
            self._reveal_adjacent_cells(row, col)
        
        return False  # Safe cell revealed
    
    def _reveal_adjacent_cells(self, row, col):
        """
        Description: Recursively reveal adjacent cells when a cell with 0 adjacent mines is revealed.
        Args:
            row (int): Row position of cell with 0 adjacent mines
            col (int): Column position of cell with 0 adjacent mines
        Returns: None
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - recursive revealing
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:  # Skip the cell itself
                    continue
                
                new_row, new_col = row + dr, col + dc
                if (0 <= new_row < self.ROWS and 
                    0 <= new_col < self.COLS):
                    
                    adjacent_cell = self.grid[new_row][new_col]
                    if (not adjacent_cell.is_revealed and 
                        not adjacent_cell.is_flagged and 
                        not adjacent_cell.is_mine):
                        
                        adjacent_cell.reveal()
                        self.revealed_cells += 1
                        
                        # Continue recursion if this cell also has 0 adjacent mines
                        if adjacent_cell.adjacent_mines == 0:
                            self._reveal_adjacent_cells(new_row, new_col)
    
    def toggle_flag(self, row, col):
        """
        Description: Toggle the flag state of a cell. Only allow flagging if not revealed. Unflagging always allowed.
        Args:
            row (int): Row position (0-9)
            col (int): Column position (0-9)
        Returns: bool - True if flag was toggled, False otherwise
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        if not (0 <= row < self.ROWS and 0 <= col < self.COLS):
            return False
        cell = self.grid[row][col]
        if cell.is_revealed:
            return False
        # Toggle flag
        cell.is_flagged = not cell.is_flagged
        return True
    
    def get_flag_count(self):
        """
        Description: Count the number of flags currently placed on the board.
        Args: None
        Returns: int - Number of flags placed
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - count flags
        count = 0
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.grid[row][col].is_flagged:
                    count += 1
        return count
    
    def get_remaining_mines(self):
        """
        Description: Get the number of remaining mines (total mines minus flags placed).
        Args: None
        Returns: int - Number of remaining mines to flag
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation
        return self.mine_count - self.get_flag_count()
    
    def is_game_won(self):
        """
        Description: Check if the game has been won (all non-mine cells revealed).
        Args: None
        Returns: bool - True if game is won, False otherwise
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Win if all non-mine cells are revealed
        return self.revealed_cells == self.total_safe_cells
    
    def reveal_all_mines(self):
        """
        Description: Reveal all mines on the board (called when game is lost).
        Args: None
        Returns: None
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Original implementation - reveal mines on game over
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.grid[row][col].is_mine:
                    self.grid[row][col].is_revealed = True
    
    def get_cell(self, row, col):
        """
        Description: Get the cell at the specified position.
        Args:
            row (int): Row position (0-9)
            col (int): Column position (0-9)
        Returns: Cell object or None if position is invalid
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Return cell if within bounds, else None.
        if 0 <= row < self.ROWS and 0 <= col < self.COLS:
            return self.grid[row][col]
        return None
    
    def get_board_state(self):
        """
        Description: Get a string representation of the current board state for debugging.
        Args: None
        Returns: str - String representation of the board
        Author: Tuan Vu
        Creation Date: September 14, 2025
        External Sources: N/A - Original Code
        """
        # Build a string representation of the board for debugging.
        result = "  A B C D E F G H I J\n"
        for row in range(self.ROWS):
            result += f"{row + 1:2} "
            for col in range(self.COLS):
                result += self.grid[row][col].get_display_value() + " "
            result += "\n"
        return result
    
    def get_covered_cells(self):
        """
        Description: Compile a list of all covered cells.
        Args: None
        Returns: list - List of cell objects
        Author: Alejandro Sandoval
        Creation Date: October 3, 2025
        External Sources: N/A - Original Code
        """
        cells = []
        for row in range(self.ROWS):
            for col in range(self.COLS):
                cell = self.grid[row][col]
                if not cell.is_revealed and not cell.is_flagged:
                    cells.append(cell)
        return cells
    
    def get_hidden_neighbors(self, center_row, center_col):
        """
        Description: Compile a list of all hidden cells around a cell.
        Args: None
        Returns: list - List of cell objects around cell
        Author: Alejandro Sandoval
        Creation Date: October 3, 2025
        External Sources: N/A - Original Code
        """
        cells = []
        for row in range(center_row-1, center_row+1):
            for col in range(center_col-1, center_col+1):
                cell = self.get_cell(row, col)
                if cell is not None and not cell.is_revealed:
                    cells.append(cell)
        return cells